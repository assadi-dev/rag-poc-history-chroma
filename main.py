import os
import asyncio
from dotenv import load_dotenv
from src.text_splitter.services import TextSplitterService
from src.documents_loader.services import DocumentLoaderService
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService
from src.retriever.services import RetrieverService
from src.documents_loader.mocks.document_content_mock import DEMO_DOCUMENTS
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt,ModelRequest 
from langchain_ollama import ChatOllama

load_dotenv()


async def setup_vectorstore():
    # 1. Load documents
    docs = DEMO_DOCUMENTS


    # 2. Split documents
    chunks = TextSplitterService().split_text(docs)

    # 3. Create embeddings and store in Chroma
    embedings =  EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    # 4. Add chunks to vectorstore
    vectorstore.add_documents(chunks)

    return vectorstore
    
@dynamic_prompt
def dynamic_prompt_middleware(request: ModelRequest):
    embeddings =  EmbeddingService().ollama_embeddings()
    last_query = request.state["messages"][-1].text
    vectorstore = VectorStoreService().chroma_vectorstore(embeddings)
    retrieved_docs = vectorstore.similarity_search(last_query)

    doc_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

    system_message = (
      "Tu es un assistant spécialisé en Intelligence Artificielle et en RAG, Utilise les informations suivantes pour répondre à la question:",
    f"\n\n: {doc_content}"
    )

    return system_message


async def main():
  #  vectorstore = await setup_vectorstore()

    embedings =  EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    query = "qui est tu ?"
    # 1. Create RAG chain



    llm = ChatOllama(model="llama3.2", temperature=0.7)

    agent = create_agent(llm, tools=[], middleware=[dynamic_prompt_middleware])

    for step in agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
      step["messages"][-1].pretty_print()




if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass