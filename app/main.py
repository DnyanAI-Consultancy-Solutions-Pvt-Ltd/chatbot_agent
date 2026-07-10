# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.agent import agent_graph

app = FastAPI(title="DnyanAI Agent Gateway API")

# Setup open CORS policies so your frontend website widget can call it
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []

@app.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        input_messages = []
        for msg in payload.history:
            if msg["role"] == "user":
                input_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                input_messages.append(AIMessage(content=msg["content"]))
                
        input_messages.append(HumanMessage(content=payload.message))
        
        output_state = await agent_graph.ainvoke({"messages": input_messages})
        final_reply = output_state["messages"][-1].content
        
        return {"response": final_reply}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Enforce standard production port mapping targeted by Hugging Face Spaces
    uvicorn.run("app.main:app", host="0.0.0.0", port=7860, reload=False)