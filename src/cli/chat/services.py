import os
from langchain_ollama import ChatOllama


class ChatService:
    def __init__(self, model:str, temperature:float):
        self.model = model
        self.temperature = temperature
        self.console = Console()


@dynamic_prompt
def dynamic_prompt_middleware(request: ModelRequest):
    embeddings =  EmbeddingService().ollama_embeddings()
    last_query = request.state["messages"][-1].text
    vectorstore = VectorStoreService().chroma_vectorstore(embeddings)
    retrieved_docs = vectorstore.similarity_search(last_query)

    doc_content = "\n\n".join([doc.page_content for doc in retrieved_docs])

    system_message = (
      "Tu es un assistant spécialisé en Intelligence Artificielle et en RAG, Utilise les informations suivantes pour répondre à la question:",
    f"\n\n: {doc_content} \n\n si tu ne trouve pas la réponse dans les informations ci-dessus, dis que tu ne sais pas et ne donne pas d'information qui n'est pas dans les informations ci-dessus \n\n Maintiens une conversation naturelle en tenant compte de l'historique."
    )

    return system_message

    def ollama_answer(self, query:str):
        llm = ChatOllama(model=self.model, temperature=self.temperature)
        agent = create_agent(llm, tools=[], middleware=[dynamic_prompt_middleware])

        for step in agent.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values",
        ):
            message = step["messages"][-1].pretty_print()
            return message
        
        

