import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_email: str

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    try:
        # Initialize Groq with the latest API standards
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Llama 3.3-70b is the flagship model for speed & reasoning in 2026
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are ZEN. Serious, emotional, and witty. Address the user as Sri. Keep responses concise and impactful for voice output."
                },
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Neural Link Error: {str(e)}"}
