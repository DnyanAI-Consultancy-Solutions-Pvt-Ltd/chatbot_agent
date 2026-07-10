# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.agent import agent_graph

app = FastAPI(title="DnyanAI Agent Gateway API")

# Setup CORS policies so widgets can easily talk to your backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = [] # Structure format: [{"role": "user"/"assistant", "content": "text"}]

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
        
        # Execute Graph Loop Lifecycle
        output_state = await agent_graph.ainvoke({"messages": input_messages})
        final_reply = output_state["messages"][-1].content
        
        return {"response": final_reply}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)