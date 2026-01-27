import os
from dotenv import load_dotenv

load_dotenv()

from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

# 1. Load documents
loader = WebBaseLoader("https://en.wikipedia.org/wiki/Artificial_intelligence")
docs = loader.load()

# 2. Split documents
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 3. Create embeddings and store in Chroma
vectorstore = Chroma.from_documents(
    documents=splits,
    collection_name="ai_docs",
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./db/.chroma_db"
)

# 4. Create RAG chain
llm = ChatOllama(model="llama3.2")
retriever = vectorstore.as_retriever()

chain = (retriever | llm).with_structured_output(Answer)

# 5. Ask questions
print(chain.invoke({"messages": [{"role": "user", "content": "What is AI?"}]}))