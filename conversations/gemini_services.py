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
        # Join previous history as a string, ensuring format consistency
        history_str = ''.join(history)
        
        # Build the prompt with a clear structure and example-based instructions
        return "\n".join([
            f"Previous Messages:\n{history_str}",
            f"User: {user_input}",
            "Tasks:",
            "'reply' : 'Provide a simple and clear response to the user's question'",
            "'corrections' : 'Correct the grammar and optimize the sentence for better clarity'",
            "'rating' : 'Rate the grammar quality of the user input on a scale of 0 to 10, where 10 is perfect grammar and 0 is completely incorrect'",
            "The response should always include a JSON object with the following keys: ['reply', 'corrections', 'rating']",
            "Make sure to return the fields, even if the corrections or rating are not applicable. For example:",
            "{ 'reply': 'This is a response.', 'corrections': 'No corrections needed.', 'rating': 1.0 }"
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