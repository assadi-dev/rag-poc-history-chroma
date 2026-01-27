import os
from langchain_ollama import ChatOllama
from rich.console import Console
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService
from langchain.agents import create_agent




class ChatService:
    def __init__(self, model: str, temperature: float,middleware):
        self.model = model
        self.temperature = temperature
        self.console = Console()
        self.middleware = middleware
        
    def ollama_answer(self, query: str):
        llm = ChatOllama(model=self.model, temperature=self.temperature)
        # Using the middleware defined above
        agent = create_agent(llm, tools=[],middleware=self.middleware)
      
        for step in agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values",
        ):
         
            # Capture the last message
           message = step["messages"][-1].content

        return message

     

