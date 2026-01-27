
import asyncio
from langchain_ollama import OllamaEmbeddings


class EmbeddingService:
 
   def ollama_embeddings(self)->OllamaEmbeddings:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    print("Embeddings created")
    return embeddings

   
