# main.py
from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.chat import router as chat_router

app = FastAPI(
    title="English Learning Bot",
    description="A smart chatbot to improve your English skills",
    version="1.0.0"
)

# Include routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(chat_router, prefix="/chat", tags=["Chatbot"])

@app.get("/")
async def root():
    return {"message": "Welcome to the English Learning Bot!"}