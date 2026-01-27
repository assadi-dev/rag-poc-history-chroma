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
from src.cli.services import CliService

load_dotenv()



    



async def main():
  #  vectorstore = await setup_vectorstore()

    embedings =  EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    query = "qui est tu ?"
    # 1. Create RAG chain


chatService = ChatService()
   cli = CliService()
   cli.run()




if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass