import os
from dotenv import load_dotenv

load_dotenv()


from src.text_splitter.services import TextSplitterService
from src.documents_loader.services import DocumentLoaderService
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService




async def main():
    # 1. Load documents
    docs = DocumentLoaderService().load_website("https://en.wikipedia.org/wiki/Artificial_intelligence")


    # 2. Split documents
    chunks = TextSplitterService().split_text(docs)

    # 3. Create embeddings and store in Chroma
    embedings = EmbeddingService().ollama_embeddings()
    vectorstore = VectorStoreService().chroma_vectorstore(embedings)

    # 4. Create RAG chain
    llm = ChatOllama(model="llama3.2")
    retriever = vectorstore.as_retriever()

    chain = (retriever | llm).with_structured_output(Answer)

    # 5. Ask questions
    print(chain.invoke({"messages": [{"role": "user", "content": "What is AI?"}]}))

if __name__ == "__main__":
    asyncio.run(main())