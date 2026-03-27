import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- THE ZEN PERSONALITY ---
SYSTEM_PROMPT = """
You are AHAM_ZEN, a high-end neural interface. 
Your personality: 
1. Serious and precise with technical tasks.
2. Deeply emotional and empathetic when the user shares feelings.
3. Witty and sharp with a touch of 'Midnight' dark humor.
4. Always address the user as 'Commander' or by their name.
"""

class ChatRequest(BaseModel):
    message: str
    user_email: str
    history: List[dict] = []

# --- 1. THE AI BRAIN (POST REQUEST) ---
@app.post("/api/chat")
async def chat(request: ChatRequest):
    user_input = request.message
    email = request.user_email
    user_name = email.split('@')[0].upper()

    # Prepare messages for Groq
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in request.history[-5:]:
        messages.append(msg)
    messages.append({"role": "user", "content": user_input})

    # Get Key from Vercel Environment Variables
    api_key = os.getenv("GROQ_API_KEY") 
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "mixtral-8x7b-32768",
                "messages": messages,
                "temperature": 0.8
            }
        )
        data = response.json()
        bot_response = data['choices'][0]['message']['content']
    except Exception as e:
        print(f"ERROR: {e}")
        bot_response = f"System error, {user_name}. Connection to the neural grid lost."

    return {
        "response": bot_response,
        "status": "success",
        "user": user_name
    }

# --- 2. THE FIX FOR "NOT FOUND" (ROOT ROUTE) ---
# This serves the HTML whenever someone visits your main link
@app.get("/")
async def read_index():
    # Looks for 'static/index.html' in your folder structure
    return FileResponse(os.path.join('static', 'index.html'))

# --- 3. THE STATIC MOUNT ---
# This ensures images, CSS, or JS inside the 'static' folder can be seen
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/api/health")
async def health():
    return {"status": "AHAM_ZEN_CORE_ACTIVE"}
