import os
from typing import TypedDict, Annotated, List, Dict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from src.memory.vector_store import get_vector_store
from src.memory.sql_store import get_db, UserSkills

# Load environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class AgentState(TypedDict):
    messages: List[Annotated[str, "The conversation history"]]
    context: str
    current_step: str

class CareerAgent:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0, 
            groq_api_key=GROQ_API_KEY, 
            model_name="llama-3.3-70b-versatile"
        )
        self.vector_store = get_vector_store()
        self.workflow = self._build_graph()

    def _retrieve_context(self, state: AgentState):
        """Node to retrieve context from vector store based on last message."""
        messages = state["messages"]
        last_message = messages[-1]
        
        if isinstance(last_message, HumanMessage):
             query = last_message.content
             # Retrieve similar docs
             docs = self.vector_store.similarity_search(query, k=3)
             context = "\n".join([doc.page_content for doc in docs])
             return {"context": context}
        return {"context": ""}

    def _generate_response(self, state: AgentState):
        """Node to generate response using LLM and context."""
        messages = state["messages"]
        context = state.get("context", "")
        
        system_prompt = f"""You are a helpful Career Guide Assistant.
        Use the following context to answer the user's questions about their career, rejection, or skills:
        
        Context:
        {context}
        
        If the context is empty or irrelevant, use your general knowledge but mention you don't have specific data on it.
        """
        
        # Prepare messages for LLM
        prompt_messages = [SystemMessage(content=system_prompt)] + messages
        
        response = self.llm.invoke(prompt_messages)
        return {"messages": [response]}

    def _build_graph(self):
        """Builds the LangGraph state machine."""
        workflow = StateGraph(AgentState)
        
        workflow.add_node("retrieve", self._retrieve_context)
        workflow.add_node("generate", self._generate_response)
        
        workflow.set_entry_point("retrieve")
        
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()

    def run(self, inputs):
        """Run the agent with inputs."""
        return self.workflow.invoke(inputs)
