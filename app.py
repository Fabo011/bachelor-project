import streamlit as st
import threading
import requests
import json
import time
from fastapi import FastAPI
from pydantic import BaseModel
import ollama
from fastmcp import Client
from lib.tools.tools import create_issue_tool, gmail_send_email_tool, duckduckgo_search_tool, duckduckgo_fetch_content_tool, wikipedia_get_summary_tool
import uvicorn

# -------------------------
# FASTAPI BACKEND
# -------------------------

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup_event():
    with open("mcp.json", "r") as f:
        config = json.load(f)

    app.state.mcp_client = Client(config)
    await app.state.mcp_client.__aenter__()

    tools = await app.state.mcp_client.list_tools()
    print("🔧 Available tools from MCP server:")
    for tool in tools:
        print(f"- {tool.name}")

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.mcp_client.__aexit__(None, None, None)

@app.post("/askmodel")
async def askmodel(request: PromptRequest):
    messages = [{"role": "user", "content": request.prompt}]
    use_tools = "calltool" in request.prompt.lower()

    if use_tools:
        response = ollama.chat(
            model="llama3.1",
            messages=messages,
            tools=[create_issue_tool, gmail_send_email_tool, duckduckgo_search_tool, duckduckgo_fetch_content_tool, wikipedia_get_summary_tool]
        )
    else:
        response = ollama.chat(
            model="llama3.1",
            messages=messages
        )

    llm_message = response.get("message", {}).get("content", "").strip()
    tool_calls = response.get("message", {}).get("tool_calls", [])
    tool_results = []

    if tool_calls and use_tools:
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]

            result = await app.state.mcp_client.call_tool(tool_name, args)
            raw_text = result[0].text if result else "⚠️ Tool returned no result"
            print(f"🔧 Tool `{tool_name}` Raw Result:", raw_text)

            tool_results.append({"tool": tool_name, "raw": raw_text})

    return {
        "llm_message": llm_message,
        "tool_results": tool_results
    }


def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

# -------------------------
# STREAMLIT FRONTEND
# -------------------------

@st.cache_resource
def start_backend():
    thread = threading.Thread(target=run_fastapi, daemon=True)
    thread.start()
    time.sleep(1)
    return True

start_backend()

st.set_page_config(page_title="DataDigger Chat", layout="centered")
st.title("🧠 Chat with MCP Tools")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me something..."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            res = requests.post("http://127.0.0.1:8000/askmodel", json={"prompt": prompt})
            data = res.json()

            # Always include the LLM's normal message first
            full_response = data.get("llm_message", "").strip()

            # Then add any tool results, if present
            tool_results = data.get("tool_results", [])
            if tool_results:
                parts = []
                for r in tool_results:
                    parts.append(f"\n\n**🔧 Tool `{r['tool']}` Result:**\n```\n{r['raw']}\n```")
                full_response += "".join(parts)

            if not full_response:
                full_response = "_No response from model._"

        except Exception as e:
            full_response = f"Error: {e}"

        # Typing animation
        display = ""
        for word in full_response.split():
            display += word + " "
            placeholder.markdown(display + "▌")
            time.sleep(0.01)
        placeholder.markdown(display)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
