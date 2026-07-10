# client.py
import requests
import sys

URL = "http://localhost:8000/chat"

print("====================================================")
print("🤖 DnyanAI Agent Live Chat Console Initialized")
print("Type your query below. Type 'exit' or 'quit' to end.")
print("====================================================\n")

# This list will keep track of the conversation state (chat history)
chat_history = []

while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Ending chat session. Goodbye!")
            break
            
        if not user_input.strip():
            continue

        # Send the payload to your FastAPI server
        payload = {
            "message": user_input,
            "history": chat_history
        }
        
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        
        agent_reply = response.json().get("response", "")
        print(f"\nAgent: {agent_reply}\n")
        
        # Append the exchange to memory so the agent remembers previous sentences
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": agent_reply})

    except KeyboardInterrupt:
        print("\nSession interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error connecting to server: {e}\n")