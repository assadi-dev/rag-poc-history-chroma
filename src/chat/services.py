from langchain_ollama import ChatOllama

class ChatService:
    def __init__(self):
        self.llm = "llama3.2"
        
   
    def ollama_chat(self, query):
        ChatOllama(
            model=self.llm,
            validate_model_on_init=True,
            temperature=0.1,

            )
 
      