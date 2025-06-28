from happytransformer import HappyTextToText

# Load the model
model_name = "Harshathemonster/t5-small-updated"
happy_tt = HappyTextToText("T5", model_name)

def correct(text: str) -> str:
    input_text = f"correct: {text}"  # Use plain text if 'correct:' is not needed
    result = happy_tt.generate_text(input_text)
    return result.text

# Example usage
if __name__ == "__main__":
    user_input = input("Enter text to correct: ")
    corrected = correct(user_input)
    print("\nWrong  :", user_input)
    print("Correct:", corrected)
