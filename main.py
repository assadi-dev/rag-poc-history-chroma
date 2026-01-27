import os
import asyncio
from dotenv import load_dotenv
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService
from src.cli.services import CliService
from src.cli.chat.services import ChatService
from langchain.agents.middleware import dynamic_prompt, ModelRequest

load_dotenv()



    

@dynamic_prompt
def dynamic_prompt_middleware(request: ModelRequest):
    embeddings = EmbeddingService().ollama_embeddings()
    last_query = request.state["messages"][-1].text
    vectorstore = VectorStoreService().chroma_vectorstore(embeddings)
    retrieved_docs = vectorstore.similarity_search(last_query)

    doc_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

    system_message = (
        "Tu es un assistant spécialisé en Intelligence Artificielle et en RAG, Utilise les informations suivantes pour répondre à la question:",
        f"\n\n: {doc_content} \n\n si tu ne trouve pas la réponse dans les informations ci-dessus, dis que tu ne sais pas et ne donne pas d'information qui n'est pas dans les informations ci-dessus \n\n Maintiens une conversation naturelle en tenant compte de l'historique."
    )

    return system_message

async def main():


    embedings =  EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    model = "llama3.2"
    temperature = 0.3
    chatService = ChatService(model, temperature,[dynamic_prompt_middleware])



    cli = CliService(chatService)
    cli.run()
 



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass