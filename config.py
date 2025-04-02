# config.py
class Settings:
    SECRET_KEY = "your-secret-key-here"  # Replace with a secure key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    MONGODB_URL = "mongodb://localhost:27017/"  # Local MongoDB (or use Atlas)
    GEMINI_API_KEY = "your-gemini-api-key-here"  # Get from Google

settings = Settings()