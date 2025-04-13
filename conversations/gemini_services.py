import google.generativeai as genai
from typing import List
from fastapi import HTTPException, status


class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini init failed: {str(e)}")

    def build_prompt(self, user_input: str, history: List[str]) -> str:
        return "\n".join([
            f"Previous Messages:\n{''.join(history)}",
            f"User: {user_input}",
            "Tasks:",
            "'reply' : 'your simple reply to the question'",
            "'corrections' : 'correct the grmmaer and optimise sentense'",
            "'rating' : 'rate the grammer for the User input which is given as input' ",
            "generate the message and give the response in a json format using keywords ['reply' , 'corrections' , 'rating']"
        ])

    def send(self, user_input: str, history: List[str]) -> dict:
        prompt = self.build_prompt(user_input, history)
        try:
            response = self.model.generate_content(prompt)
            reply_text = response.text

            if not reply_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Empty response from Gemini"
                )

            corrected = self.extract("Corrected", reply_text)
            suggestion = self.extract("Suggested", reply_text)
            rating = self.extract("Rating", reply_text)
            reply = self.extract("Reply", reply_text)

            return {
                "corrected": corrected or "-",
                "suggestion": suggestion or "-",
                "rating": float(rating) if rating else 0.0,
                "reply": reply or reply_text  # fallback to full response if label not found
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Gemini Error: {str(e)}"
            )

    def extract(self, label: str, text: str) -> str:
        for line in text.splitlines():
            if line.lower().startswith(label.lower() + ":"):
                return line.split(":", 1)[1].strip()
        return ""