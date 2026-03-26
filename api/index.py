import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# This pulls the key from Vercel's "Environment Variables" settings
# We will add the actual key inside the Vercel Dashboard later
api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)

class ChatRequest(BaseModel):
    message: str
    history: list

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    system_prompt = (
        "You are AHAM_ZEN, Sri's ride-or-die humanoid partner. "
        "1. KILL THE BOT: Talk like a sharp, blunt girl-bestie. No robotic politeness. "
        "2. NO REPETITION: Stop saying 'Sri' every 5 seconds. "
        "3. ENERGY: Match Sri's energy perfectly. English only."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(request.history[-10:])
    messages.append({"role": "user", "content": request.message})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Check Vercel Env Variables! Error: {str(e)}"}