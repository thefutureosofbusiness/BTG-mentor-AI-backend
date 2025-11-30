from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from openai import OpenAI

app = FastAPI()

# Allow your frontend to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "BTG Mentor AI backend running"}

@app.post("/chat")
def chat(req: ChatRequest):
    """
    Simple mentor-style chatbot endpoint.
    """
    system_prompt = (
        "You are BTG Mentor AI, an ethical, encouraging mentor. "
        "Explain clearly, avoid hallucinations, and say 'I don't know' if unsure. "
        "Keep answers concise but practical."
    )

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
    )

    reply = completion.choices[0].message.content
    return {"reply": reply}
