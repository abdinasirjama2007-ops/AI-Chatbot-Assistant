import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Load .env for local dev
load_dotenv()

# --- OpenAI client (official SDK) ---
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    client = None

# --- FastAPI app ---
app = FastAPI(title="AI Chatbot Assistant", version="1.0.0")

# CORS (open by default; lock down origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# --- Schemas ---
class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = (
        "You are an intelligent, concise assistant. Be helpful, accurate, and clear."
    )
    model: Optional[str] = "gpt-4o-mini"  # adjust to your available model
    temperature: Optional[float] = 0.3
    max_tokens: Optional[int] = 400

class ChatResponse(BaseModel):
    reply: str

# --- Routes ---
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message or not req.message.strip():
        raise HTTPException(status_code=400, detail="Message must not be empty.")

    # Fallback if no OpenAI key
    if client is None or not os.getenv("OPENAI_API_KEY"):
        # Tiny rule-based fallback so the app still runs without a key.
        reply = f"(Local fallback) You said: {req.message.strip()}"
        return ChatResponse(reply=reply)

    try:
        # Use Responses API (chat-style)
        result = client.chat.completions.create(
            model=req.model,
            messages=[
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.message},
            ],
            temperature=req.temperature,
            max_tokens=req.max_tokens,
        )
        reply = result.choices[0].message.content.strip()
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {e}")
