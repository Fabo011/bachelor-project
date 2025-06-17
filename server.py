from fastapi import FastAPI
from pydantic import BaseModel
from mcp_use import MCPClient, MCPAgent
import asyncio

from lib.model.model import llm_wrapper  # your wrapper with .bind_tools

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup_event():
    client = MCPClient.from_config_file("mcp.json")
    agent = MCPAgent(llm=llm_wrapper, client=client, max_steps=20)
    await agent.initialize()
    app.state.mcp_client = client
    app.state.mcp_agent = agent

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.mcp_client.close_all_sessions()
    await app.state.mcp_agent.close()

@app.post("/askmodel")
async def askmodel(request: PromptRequest):
    agent = app.state.mcp_agent
    llm_result = await agent.run(request.prompt)

    if hasattr(llm_result, "generations"):
        first_gen = llm_result.generations[0][0]
        response_text = first_gen.message.content
    elif isinstance(llm_result, str):
        response_text = llm_result
    else:
        response_text = str(llm_result)

    return {"llm_response": response_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)





    