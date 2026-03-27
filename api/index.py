import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.responses import HTMLResponse

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_email: str

# FIX: This handles the "Home" page so you don't get a 404/Not Found
@app.get("/")
async def read_root():
    return {"status": "ZEN_CORE_ONLINE", "message": "Ready for input, Sri."}

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are ZEN. Serious, emotional, and witty. Address user as Sri."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Neural Error: {str(e)}"}
