# gemini_service.py

import google.generativeai as genai # type: ignore
from typing import List
from fastapi import HTTPException
import ast
class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        try:
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gemini init failed: {str(e)}")

    def build_prompt(self, user_input: str, history: List[str]) -> str:
        history_str = "\n".join(history)  # better formatting with line breaks

        return "\n".join([
            f"Previous Messages:\n{history_str}",
            f"User: {user_input}",
            "Tasks:",
            "'reply': 'Provide a simple and clear response to the user's question'",
            "'corrections': 'Correct the grammar and optimize the sentence for better clarity'",
            "'rating': 'Rate the grammar quality of the user input on a scale of 0 to 10, where 10 is perfect grammar and 0 is completely incorrect'",
            "The response must be in JSON format with keys: ['reply', 'corrections', 'rating']",
            "Example:",
            "{ 'reply': 'This is a response.', 'corrections': 'No corrections needed.', 'rating': 1.0 }",
            "Return only the raw JSON object. Do not use Markdown or ```json formatting."
        ])

    def send(self, user_input: str, history: List[str]) -> dict:
        prompt = self.build_prompt(user_input, history)
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            response_dict = ast.literal_eval(response_text)  # safer than eval()

            if isinstance(response_dict, dict):
                return response_dict
            else:
                raise ValueError("Response is not a dictionary.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to parse Gemini response: {str(e)}")
