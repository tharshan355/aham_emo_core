import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

# This is the secret sauce: it mounts your UI folder so Vercel can't miss it
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str
    user_email: str

# This specifically fixes the {"detail":"Not Found"} error on the home page
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return {"response": "System Error: GROQ_API_KEY is missing in Vercel settings."}

        client = Groq(api_key=api_key)
        
        # Using Llama 3.3-70b for speed and to avoid decommissioned model errors
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are ZEN. Serious, emotional, and witty. Address the user as Sri. Keep responses short for voice."
                },
                {"role": "user", "content": request.message}
            ],
            temperature=0.7
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Neural Link Error: {str(e)}"}
