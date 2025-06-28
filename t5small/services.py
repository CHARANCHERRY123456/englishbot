import google.generativeai as genai  # type: ignore
from typing import List
from fastapi import HTTPException
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Path to your fine-tuned model on Hugging Face
model_path = "Harshathemonster/t5-small-updated"

class T5Service:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.model = self.model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        print("Grammar corrector initialized")

    def correct(self, text: str) -> str:
        print("Correcting grammar for:", text)
        prompt = f"correct: {text}"

        input_ids = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=128).input_ids
        input_ids = input_ids.to(self.model.device)

        outputs = self.model.generate(
            input_ids,
            max_length=128,
            num_beams=4,
            early_stopping=True
        )

        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text.strip()

# # Instantiate service
# gemini = T5Service()
# print("Gemini service initialized")

# # Test inputs
# sentences = ["hi i are charan", "waht is not you doing", "i am not going to the store"]

# for sentence in sentences:
#     corrected = gemini.correct(sentence)
#     print(f"Original: {sentence}")
#     print(f"Corrected: {corrected}\n")
