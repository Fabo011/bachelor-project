from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import json
from fastmcp import Client
from lib.tools.tools import create_issue_tool

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup_event():
    with open("mcp.json", "r") as f:
        config = json.load(f)

    app.state.mcp_client = Client(config)
    await app.state.mcp_client.__aenter__()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.mcp_client.__aexit__(None, None, None)

@app.post("/askmodel")
async def askmodel(request: PromptRequest):
    messages = [{"role": "user", "content": request.prompt}]

    response = ollama.chat(
        model="llama3.1",
        messages=messages,
        tools=[create_issue_tool]
    )

    tool_calls = response.get("message", {}).get("tool_calls", [])
    if tool_calls:
        tool_call = tool_calls[0]
        tool_name = tool_call["function"]["name"]
        args = tool_call["function"]["arguments"]

        # call MCP tool async
        result = await app.state.mcp_client.call_tool(tool_name, args)

        try:
            parsed_result = json.loads(result[0].text)
        except Exception:
            parsed_result = result[0].text

        return {"llm_response": f"Tool '{tool_name}' called successfully with result: {parsed_result}"}

    return {"llm_response": response["message"]["content"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
