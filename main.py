import os
import asyncio
import uuid
from dotenv import load_dotenv
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService
from src.cli.services import CliService
from src.cli.chat.services import ChatService
from langchain.agents.middleware import dynamic_prompt, ModelRequest

load_dotenv()



    

@dynamic_prompt
def dynamic_prompt_middleware(request: ModelRequest):
    # 1. Récupérer le dernier message utilisateur (robuste)
    last_user_message = request.state["messages"][-1].text

    # 2. RAG
    embeddings = EmbeddingService().ollama_embeddings()
    last_query = last_user_message
    vectorstore = VectorStoreService().chroma_vectorstore(embeddings)
    retrieved_docs = vectorstore.similarity_search(last_query,k=5)

    doc_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

    if not retrieved_docs:
        return (
            "Aucune information pertinente n’a été trouvée dans la base de connaissances. "
            "Si la réponse n’est pas présente dans le contexte fourni, réponds explicitement "
            "que tu ne sais pas."
        )

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # 3. System prompt RAG strict
    system_prompt = f"""
        Tu es un assistant expert en Intelligence Artificielle et en RAG.

        Règles strictes :
        - Utilise UNIQUEMENT les informations du contexte ci-dessous
        - Si la réponse n’est pas présente dans le contexte, dis clairement que tu ne sais pas
        - N’invente aucune information
        - Réponds de manière naturelle en tenant compte de l’historique de la conversation

        Contexte :
        {context}
        """.strip()

    return system_prompt


async def main():
    thread_id = str(uuid.uuid4())
    user_id = "1"

    embedings =  EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    model = "llama3.2"
    temperature = 0.3
    chatService = ChatService(model, temperature,[dynamic_prompt_middleware],thread_id,user_id)



    cli = CliService(chatService)
    cli.run()
 



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass