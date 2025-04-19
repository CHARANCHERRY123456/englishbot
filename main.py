from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logger import logger
from auth.routes import router as auth_router
from conversation.routes import router as conversation_router
from message.routers import router as message_router

logger.info("Starting FastAPI application...")

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

app.include_router(router=auth_router,prefix="/auth",tags=["auth"])
app.include_router(router=conversation_router,prefix="/conversation",tags=["conversation"])
app.include_router(router=message_router , prefix="/message" , tags=["message"])

@app.get("/")
def root():
    return {"satus": "ok", "message": "Welcome to the English Learning Chatbot API!"}
