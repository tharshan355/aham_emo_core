from fastapi import FastAPI, Request
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.post("/api/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_msg = data.get("message", "")
        
        # Fast 8b model to prevent timeouts
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are AHAM, a witty and emotional AI for Sri. Keep it cool and high-tech."},
                {"role": "user", "content": user_msg}
            ]
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Internal Error: {str(e)}"}
