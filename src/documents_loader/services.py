import asyncio
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import CSVLoader
from langchain_community.document_loaders import WebBaseLoader
import bs4

class DocumentLoaderService:
    async def load_website(self, url: str) -> str:
        bs4_strainer = bs4.SoupStrainer(class_=("post-title", "post-header", "post-content"))
        loader = WebBaseLoader(
            web_paths=(url),
            bs_kwargs={"parse_only": bs4_strainer},
        )
        docs = await loader.aload()
        print("Contenu du site web chargé")

        return docs
    
    async def load_pdf(self, file_path: str) -> str:
        pass
    
    async def load_txt(self, file_path: str) -> str:
        loader = DirectoryLoader(file_path, glob="**/*.txt")
        docs = await loader.aload()
        print("Contenu du fichier texte chargé")
        
        return docs
    
    async def load_docx(self, file_path: str) -> str:
        pass
    
    async def load_csv(self, file_path: str) -> str:
        pass
    
    async def load_json(self, file_path: str) -> str:
        pass
    
    
    async def load_md(self, file_path: str) -> str:
        pass


  