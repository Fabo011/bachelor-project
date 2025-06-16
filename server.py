from fastapi import FastAPI
from mcp_use import MCPClient
from gpt4all import GPT4All
import os

app = FastAPI()

MODEL_NAME = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
MODEL_DIR = os.path.expanduser("~/.cache/gpt4all")
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

os.makedirs(MODEL_DIR, exist_ok=True)

if not os.path.exists(MODEL_PATH):
    print(f"Model not found at {MODEL_PATH}, downloading...")
else:
    print(f"Model found at {MODEL_PATH}, using local copy.")

model = GPT4All(MODEL_NAME, model_path=MODEL_DIR)

#client = MCPClient.from_config_file("mcp.json")
#client.add_server("Zapier")
#zapier = client.zapier


@app.post("/test")
async def test():
    prompt = "What is the best place in Malaga to visit? "
    llm_response = model.generate(prompt)
    print(llm_response)

    # Optional: actually send via Zapier
    # result = await zapier.call("gmail_send_email", {
    #     "to": "based011@protonmail.com",
    #     "subject": "Best places in Malaga",
    #     "body": email_body
    # })

    return {
        "llm_response": llm_response,
        # "email_send_result": result
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





