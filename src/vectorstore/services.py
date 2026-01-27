from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


class VectorStoreService:
    def __init__(self):
        pass

    def chroma_vectorstore(self, embeddings) -> Chroma:
        """Initialise ou charge le vectorstore Chroma."""
        embedding_fn = embeddings
        
        if embedding_fn is None:
            raise ValueError("Une fonction d'embedding doit être fournie soit à l'initialisation, soit à la méthode.")
            
        vectorstore = Chroma(
            collection_name="ai_docs",
            embedding_function=embedding_fn,
            persist_directory="../databases/.chroma_db"
        )
        return vectorstore