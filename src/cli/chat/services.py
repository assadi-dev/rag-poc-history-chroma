import os
from langchain_ollama import ChatOllama
from rich.console import Console
from src.embedding.services import EmbeddingService
from src.vectorstore.services import VectorStoreService
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import ChatPromptTemplate



class ChatService:
    def __init__(self, model: str, temperature: float,middleware,thread_id:str,user_id:str):
        self.model = model
        self.temperature = temperature
        self.console = Console()
        self.middleware = middleware
        self.checkpointer = InMemorySaver()
        self.thread_id = thread_id
        self.user_id = user_id
        
    def ollama_answer(self, query: str):
        llm = ChatOllama(model=self.model, temperature=self.temperature)
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "You are a helpful assistant. Your name is Alex."),
                ("human", "{question}"),
            ]
        )
        inputs =  {"messages": prompt_template.format_messages(question=query)}
        agent = create_agent(llm, tools=[],middleware=self.middleware,checkpointer=self.checkpointer)

      
        for step in agent.stream(
            inputs ,
            config={"configurable": {"thread_id": self.thread_id,"user_id": self.user_id}},
            stream_mode="values",
        ):
       
            # Capture the last message
           message = step["messages"][-1].content

        return message

     

