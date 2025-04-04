from google import genai
from PIL import Image
# from config import settings
from config import settings
client = genai.Client(api_key=settings.GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["whaat are you doing","can you please optimise and correct the grammer in this and just give the simple one line answer"])
print(response.text)