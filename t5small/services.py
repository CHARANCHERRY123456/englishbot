# gemini_service.py

import google.generativeai as genai # type: ignore
from typing import List
from fastapi import HTTPException
# import ast
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_path = "Harshathemonster/t5-grammar-corrector"

class GeminiService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        print("Grammar corrector initialized")
        
    def correct(self, text:str) -> dict:
        #Use model to correct grammar
        print("Correcting grammar")
        prompt = f"grammar : {text}"

        #Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt")
        print("inputs : ", inputs)

        #Generate Output 
        outputs = self.model.generate(**inputs, max_length=128)
        print("outpust : ", outputs)

        #Decode 
        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("correcrted : ", corrected_text)

        print("Grammar corrected")
        return {"corrected_text": corrected_text}
    
gemini = GeminiService()    
print("Gemini service initialized")
# def build_prompt(user_input: str, history: List[str]) -> str:
response = gemini.correct("He went to school everyday")
print(response["corrected_text"])