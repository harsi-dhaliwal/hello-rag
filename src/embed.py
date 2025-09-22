from typing import List
from openai import OpenAI
from config import settings

def get_client()-> OpenAI:
    api_key = settings.openai_api_key
    return OpenAI(api_key=api_key)

def embed_texts(texts:List[str],model:str|None = None) -> List[List[float]]:
    client = get_client()
    model = model or settings.model
    resp = client.embeddings.create(model=model,input=texts)
    return [d.embedding for d in resp.data]