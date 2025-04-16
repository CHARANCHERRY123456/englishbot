# from google import genai
# from PIL import Image
# # from config import settings
# from ..config import settings
# client = genai.Client(api_key=settings.GEMINI_API_KEY)
# response = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=["whaat are you doing","can you please optimise and correct the grammer in this and just give the simple one line answer"])
# print(response.text)

import google.generativeai as types
from google import genai
from dotenv import load_dotenv
load_dotenv()
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

chat = client.chats.create(model='gemini-2.0-flash-001')

response = chat.send_message('tell me a story')
print(response.text)

response = chat.send_message("what i asked you before")
print(response.text)


# genai.configure(api_key=GEMINI_API_KEY)

# # Create a chat session with memory
# chat = genai.GenerativeModel("gemini-pro").start_chat(history=[])

# response = chat.send_message("Hello!")
# print(response.text)

# # Send follow-up
# response = chat.send_message("What did I just ask?")
# print(response.text)
