# app/agent.py
import os
from typing import Annotated, TypedDict, Literal
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()

# Force HuggingFace to download embedding weights to /tmp instead of read-only root directories
os.environ["HF_HOME"] = "/tmp/.cache"

# Initialize local embeddings and point vector store path to /tmp/database
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
vectorstore = Chroma(persist_directory="/tmp/database", embedding_function=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

@tool
def query_company_knowledge_base(query: str) -> str:
    """Search the official DnyanAI documentation for information regarding software services, Generative AI labs, consulting tracks, and training offerings."""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

tools = [query_company_knowledge_base]
tool_node = ToolNode(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Hooking up stable Groq model engine
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1).bind_tools(tools)

SYSTEM_PROMPT = SystemMessage(
    content="You are an autonomous conversational Agent for DnyanAI (AI/ML Solutions, Training & Consulting company).\n"
    "Your objective is to answer user queries using the 'query_company_knowledge_base' tool when asked about services, capabilities or modules.\n"
    "Rules:\n"
    "1. Only answer questions based on retrieved knowledge base info. If details aren't found, state that you don't possess that specific data and ask for their email to let a human engineer reply.\n"
    "2. If the user asks to schedule a call or work together, explicitly guide them to drop their contact email address right here in the chat."
)

def call_model(state: AgentState):
    messages = [SYSTEM_PROMPT] + state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"

workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

agent_graph = workflow.compile()