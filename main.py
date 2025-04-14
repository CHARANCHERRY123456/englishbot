from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from dotenv import load_dotenv
load_dotenv()
from oorke import get_uri

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="English Learning Chatbot API",
    description="A chatbot API to help users practice English with conversation history and grammar correction"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def root():
    return {"satus": "ok", "message": "Welcome to the English Learning Chatbot API!"}
