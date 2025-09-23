from fastapi import FastAPI
from pydantic import BaseModel

from embed import get_client
from search import search
from answer import build_prompt
from config import settings

settings.validate(require_api=True)
app = FastAPI()

class ChatRequest(BaseModel):
    message:str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    results = search(user_message,"data/processed/index.pkl")
    if not results:
        return {"response": "No results found"}

    prompt, uniq_sources = build_prompt(user_message, results)

    client = get_client()
    resp = client.chat.completions.create(
        model=settings.chat_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    answer = resp.choices[0].message.content
    return {"response":answer,"sources":uniq_sources}