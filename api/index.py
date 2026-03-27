import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_email: str

# FIX: This stops the "Not Found" error if you visit the API directly
@app.get("/api")
async def root():
    return {"status": "ZEN_CORE_ONLINE", "user": "Sri"}

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Using Llama 3.3 to avoid the 'decommissioned' error
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are ZEN. Serious, emotional, and witty. Address the user as Sri. Keep responses short."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Neural Link Error: {str(e)}"}
