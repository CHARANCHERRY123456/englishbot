from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from routes.conversation_routes import router as conversation_router
from routes.message_routes import router as message_router
from routes.auth import router as auth_router
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="English Learning Chatbot API",
    description="A chatbot API to help users practice English with conversation history and grammar correction"
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(conversation_router, prefix="/conversation", tags=["Conversations"])
app.include_router(message_router, prefix="/message", tags=["Messages"])



@app.get("/")
def root():
    return {"status": "ok", "message": "English Learning Chatbot API is running"}
