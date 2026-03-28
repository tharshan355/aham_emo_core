import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str
    user_email: str

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are ZEN, a smart, clear, and professional female AI. Be helpful and polite. Always address the user as Sri."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception:
        return {"response": "I'm having trouble connecting, Sri. Please check the network."}
