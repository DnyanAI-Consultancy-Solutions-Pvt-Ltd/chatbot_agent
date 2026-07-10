# chatbot_agent
Chtabot_agent for DnyanAI-Consultancy-Solutions-Pvt-Ltd

# DnyanAI Autonomous RAG Chatbot Agent

An enterprise-grade, autonomous **Retrieval-Augmented Generation (RAG)** chatbot agent engineered for **DnyanAI**. This system dynamically crawls, tokenizes, and indexes your website content locally, allowing an LLM agent orchestration loop to accurately answer customer inquiries without hallucinations.

The architecture uses **LangGraph** for multi-step agent reasoning, a local **Chroma DB** combined with **HuggingFace Embeddings** for zero-cost semantic search, **Groq API** (`llama-3.3-70b-versatile`) for blazing-fast inference, and **FastAPI** as the async API gateway.

---

## 📂 Project Directory Structure

```text
dnyanai-agent/
│
├── database/                # Local persistent vector database storage (ChromaDB)
├── app/
│   ├── __init__.py
│   ├── agent.py             # Core LangGraph agent loop & tool binding definition
│   └── main.py              # FastAPI server gateway backend
│
├── .env                     # Private environment configurations (API Keys)
├── requirements.txt         # Backend Python application dependencies
├── ingest.py                # Web scraper and text chunk embedding initializer
└── client.py                # Command Line interactive chat tester interface

🛠️ Installation & Environment Setup
1. Clone or Move to Your Project Folder
Open your terminal/PowerShell and navigate to your project workspace:

PowerShell: cd C:\Chatbot

2. Configure Your Virtual Environment (Python 3.11 Pinned)
Ensure your workspace is isolated using a Python 3.11 engine profile to avoid package conflicts:

# Create the virtual environment using Python 3.11
py -V:3.11 -m venv .venv

# Activate the virtual environment (Windows PowerShell)
.venv\Scripts\Activate.ps1

3. Install Dependencies & Update Chroma Architecture

# Install primary requirements
pip install -r requirements.txt

# Install supplemental text processing tools
pip install sentence-transformers langchain-groq langchain-huggingface

# Enforce update to prevent dependency resolver conflicts
pip install -U chromadb

4. Configure Application Secrets
Create a .env file in the root project directory and paste your Groq credentials:

GROQ_API_KEY=gsk_yourActualGroqApiKeyHere

🚀 Running the Application Lifecycle
Step 1: Ingest Website Documentation
Run the ingestion engine to parse the live domain links, chunk the text strings, and generate vectors:
python ingest.py : (Expected Output: Vector database successfully built locally via HuggingFace inside ./database.)

Step 2: Spin Up the FastAPI Backend Gateway Server
Launch the asynchronous Uvicorn interface framework: 
python -m app.main - (Expected Output: INFO: Application startup complete. Uvicorn running on http://0.0.0.0:8000)

Step 3: Start Interactive Chat Session (Testing CLI Client)
Open a separate terminal shell, activate your environment, and spin up the live console script to chat with the agent:

python client.py

🌐 API Interaction Documentation
Interactive Swagger Docs
Once the backend server is running, navigate your web browser to:
👉 http://localhost:8000/docs

This allows you to execute, trace, and evaluate payload outputs instantly using a clean, native UI.

Direct API Endpoint Payload Spec
URL: http://localhost:8000/chat

Method: POST

Headers: Content-Type: application/json

Request Body Structure:

{
  "message": "What services does DnyanAI offer?",
  "history": [
    {"role": "user", "content": "Hello bot!"},
    {"role": "assistant", "content": "Hello! How can I help you learn about DnyanAI today?"}
  ]
}

🛡️ Core Agent Directives & Guardrails
The agent is explicitly programmed via a foundational system architecture design script to:

Enforce Absolute Grounding: Only answer prompts based on information verified within the scraped website context vector matrix.

Prevent Hallucinations: Politely refuse to make up operational information or answer abstract non-company related prompts.

Optimized Sales Lead Generation: Automatically identify booking intents or general collaboration targets and prompt users to leave an explicit email address for follow-ups.

