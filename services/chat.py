import requests
from config import settings
from db import conversations_collection

# currently doing it with gemini api key 
def process_message(message:str,username:str):
    url="https://api.gemini.google.com/v1/completions"
    headers={
        "Autherization" : f"Bearer {settings.GEMINI_API_KEY}"
    }
    payload = {
        "prompt": f"Correct the grammar and optimize this sentence: {message}",
        "max_tokens": 100
    }

    try:
        response = requests.post(url,json=payload,headers=headers)
        response.raise_for_status()
        corrected_message = response.json().get("choices", )
    except Exception as e:
        pass