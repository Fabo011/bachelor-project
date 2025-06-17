from fastapi import FastAPI
from lib.api.askmodel import PromptRequest, generate_response, send_email_via_mcp

app = FastAPI()

@app.post("/askmodel")
async def askmodel(request: PromptRequest):
    llm_response = generate_response(request.prompt)
    if "plant needs water" in llm_response.lower():
      mcp_result = await send_email_via_mcp(llm_response)
    return {"llm_response": llm_response, "mcp_result": mcp_result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    