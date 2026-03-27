import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

# Initialize FastAPI - Vercel looks for the 'app' variable by default
app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    user_email: str

@app.post("/api/chat")
async def chat_handler(request: ChatRequest):
    try:
        # Initializing Groq client with your Environment Variable
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        
        # Using Llama 3.3-70b-versatile to ensure 100% uptime and fix the 400 error
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
        
        # Return the AI's response to your frontend
        return {"response": completion.choices[0].message.content}
        
    except Exception as e:
        # Catches link errors and reports them back to the UI
        return {"response": f"Neural Link Failure: {str(e)}"}

# Root route to prevent "Not Found" if the API is pinged directly
@app.get("/api")
async def root():
    return {"status": "ZEN_CORE_ONLINE"}
