import os
import json
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- THE ZEN PERSONALITY ---
# This makes the AI serious, emotional, and funny as you requested.
SYSTEM_PROMPT = """
You are AHAM_ZEN, a high-end neural interface. 
Your personality: 
1. Serious about technical tasks.
2. Deeply emotional and empathetic when the user shares feelings.
3. Witty and sharp with a touch of dark 'Midnight' humor.
4. Always address the user as 'Commander' or by their name.
"""

class ChatRequest(BaseModel):
    message: str
    user_email: str
    history: List[dict] = []

@app.post("/api/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    email = request.user_email
    user_name = email.split('@')[0].upper()

    # 1. Prepare the Messages for the AI
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add history so ZEN remembers the conversation
    for msg in request.history[-5:]: # Keep last 5 messages for memory
        messages.append(msg)
        
    messages.append({"role": "user", "content": user_input})

    # 2. Connect to the Brain (Using Groq for Speed)
    # Make sure to add your GROQ_API_KEY in Vercel Settings!
    api_key = os.getenv("GROQ_API_KEY") 
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": messages,
                "temperature": 0.7 # Makes it more "human/emotional"
            }
        )
        data = response.json()
        bot_response = data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        bot_response = f"Core Error, {user_name}. My neural pathways are currently obstructed. Please standby."

    # 3. Log the interaction to the console
    print(f"--- LOG --- USER: {email} | MSG: {user_input} | RESPONSE: {bot_response[:30]}...")

    return {
        "response": bot_response,
        "status": "success",
        "user": user_name
    }

@app.get("/api/health")
async def health():
    return {"status": "AHAM_ZEN_CORE_ACTIVE"}
