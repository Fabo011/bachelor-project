from pydantic import BaseModel
from lib.model.model import load_model

# Load model once
model = load_model()

class PromptRequest(BaseModel):
    prompt: str

def generate_response(prompt: str) -> str:
    response = model.generate(prompt, max_tokens=1000)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    return response