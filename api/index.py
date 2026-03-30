from fastapi import FastAPI, Request
from groq import Groq
import os

app = FastAPI()

# Make sure you set GROQ_API_KEY in Vercel Environment Variables
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.post("/api/chat")
async def chat_handler(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "")

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # LIGHTNING FAST MODEL
            messages=[
                {"role": "system", "content": "You are AHAM, a witty, emotional AI for Sri. Keep answers punchy and cool."},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}
