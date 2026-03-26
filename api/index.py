from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# This is CRITICAL for the web reply to work
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key="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")

class ChatRequest(BaseModel):
    message: str
    history: list

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    system_prompt = "You are AHAM_ZEN, Sri's ride-or-die partner. Sharp, blunt girl-bestie personality. English only."
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(request.history[-10:])
    messages.append({"role": "user", "content": request.message})

    try:
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages)
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
