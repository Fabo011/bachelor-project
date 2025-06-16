from fastapi import FastAPI
from lib.api.askmodel import PromptRequest, generate_response

app = FastAPI()

@app.post("/askmodel")
async def askmodel(request: PromptRequest):
    llm_response = generate_response(request.prompt)
    return {"llm_response": llm_response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    