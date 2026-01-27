from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class VectorStoreService:
    def __init__(self,embeddings:OllamaEmbeddings):
        self.vectorstore = None

    def chroma_vectorstore(self):
        vectorstore = Chroma(
            collection_name="ai_docs",
            embedding_function=embeddings,
           persist_directory="../databases/.chroma_db"
        )
        return vectorstore