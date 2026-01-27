import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


from src.text_splitter.services import TextSplitterService
from src.documents_loader.services import DocumentLoaderService
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService
from src.retriever.services import RetrieverService
from src.documents_loader.mocks.document_content_mock import DEMO_DOCUMENTS




async def main():
    # 1. Load documents
    docs = DEMO_DOCUMENTS


    # 2. Split documents
    chunks = TextSplitterService().split_text(docs)

    # 3. Create embeddings and store in Chroma
    embedings =  EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    # 4. Add chunks to vectorstore
    vectorstore.from_documents(chunks, embedings)

    # 5. Create RAG chain
   # llm = ChatOllama(model="llama3.2")
   # retriever = RetrieverService().chroma_retriever_by_similarity(vectorstore, "What is AI?")

  #  chain = (retriever | llm).with_structured_output(Answer)

    # 5. Ask questions
  #  print(chain.invoke({"messages": [{"role": "user", "content": "What is AI?"}]}))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass