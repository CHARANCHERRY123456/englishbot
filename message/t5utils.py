
from t5small.services import T5Service
from typing import List
from fastapi import HTTPException

t5service = T5Service()
print("T5 service initialized")

async def get_answer_using_t5(text: str) -> str:
    """
    Get answer using T5 model
    """
    try:
        response = t5service.correct(text)
        return response
    except Exception as e:
        # Log the exception or handle it as needed
        print(f"An error occurred while getting a reply from T5: {e}")
        return "Sorry, I couldn't process your request."