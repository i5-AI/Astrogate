import requests
from server.python.config import OPENAI_API_KEY

def create_embeddings(text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "input": text,
        "model": "text-embedding-ada-002"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()
