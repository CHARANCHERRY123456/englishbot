from fastapi import FastAPI, HTTPException
from google import genai
from config import settings  # Ensure this contains GEMINI_API_KEY

app = FastAPI()
# client = genai.Client(settings.GEMINI_API_KEY)
client = genai.Client(api_key=settings.GEMINI_API_KEY)

@app.post("/correct-grammar/")
def process_message(message: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[message,"can you please optimise and correct the grammer in this and just give the simple one line answer"])
        return response.text
    except Exception as e:
        print(e)
        return "Sorry someting happend in the internal sever"

