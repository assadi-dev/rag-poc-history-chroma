from langchain_chroma import Chroma
from typing import List
from langchain_core.documents import Document

class RetrieverService:
    
    def chroma_retriever_by_similarity(self, vectorstore: Chroma, query: str) -> List[Document]:
        """Effectue une recherche par similitude et retourne les documents correspondants."""
        result = vectorstore.similarity_search(query, k=5)
        for doc in result:
            print(doc.page_content)
            print("-"*50)
        return result
