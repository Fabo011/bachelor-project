import os
from gpt4all import GPT4All

def load_model():
    MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
    MODEL_DIR = os.path.expanduser("~/.cache/gpt4all")
    MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

    os.makedirs(MODEL_DIR, exist_ok=True)

    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}, downloading...")
    else:
        print(f"Model found at {MODEL_PATH}, using local copy.")

    return GPT4All(MODEL_NAME, model_path=MODEL_DIR)