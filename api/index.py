import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq

# Initialize FastAPI
app = FastAPI()

# System Personality Profile
SYSTEM_PROMPT = """
You are AHAM_ZEN, a high-end neural interface. 
Your personality: 
1. Serious and precise with technical tasks.
2. Deeply emotional and empathetic when the user shares feelings.
3. Witty and sharp with a touch of 'Midnight' dark humor.
4. Address the user as 'Commander' or 'Sri'.
"""

# Data model for incoming requests
class ChatRequest(BaseModel):
    message: str
    user_email: str
    history: Optional[List[dict]] = []

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    # 1. Verify API Key exists in Vercel Environment
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return JSONResponse(
            status_code=500,
            content={"response": "Neural link failure: GROQ_API_KEY missing in server environment."}
        )

    try:
        # 2. Initialize Groq Client
        client = Groq(api_key=api_key)
        
        # 3. Build Message Thread
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add history if provided (last 5 messages for context)
        if request.history:
            messages.extend(request.history[-5:])
            
        # Add current user message
        messages.append({"role": "user", "content": request.message})

        # 4. Generate AI Completion
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=messages,
            temperature=0.75,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # 5. Extract and Return Response
        response_text = completion.choices[0].message.content
        return {"response": response_text, "status": "success"}

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"response": f"Core Exception: {str(e)}", "status": "error"}
        )

# Health check route for Vercel monitoring
@app.get("/api/health")
async def health():
    return {"status": "AHAM_ZEN_CORE_ONLINE"}
