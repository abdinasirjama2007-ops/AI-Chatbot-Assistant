# 🤖 AI Chatbot Assistant

A minimal FastAPI + OpenAI chatbot with a clean, zero-dependency front-end.

## Quickstart

```bash
git clone <your-repo-url>
cd ai-chatbot-assistant
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env && nano .env                   # add your OPENAI_API_KEY
uvicorn app:app --reload
