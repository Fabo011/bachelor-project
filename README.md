# AI Workflow

## Installation

Disclaimer: This is made and tested on Apple M1.

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

```
brew install ollama
ollama pull llama3
ollama pull MFDoom/deepseek-v2-tool-calling:latest
ollama create deepseek-lite -f Modelfile
```

Delete models which are no longer needed
```
ollama rm <model-name>
```

**Start Server**
```
uvicorn server:app --reload
ollama serve
```

---

### Prompt for the model
You are an agent with access to a tool called create_issue, which creates GitHub issues using an MCP server. Please create an issue in the GitHub repository owned by 'Fabo011' and named 'bachelor-project'. The issue should describe a bug or feature related to 'Add unit tests for the API endpoints'. You must decide an appropriate issue title and detailed body description for this topic.

---

### Ollama
A local model server + CLI for running and managing open-source LLMs (LLaMA, Mistral, etc.).

---

### MCP
Ollama tools calls the connected mcp servers based on the prompt.

---

### Modelfile
Configurations for the LLM. I`ve changed the parameters to run it on Mac M1 with 16gb RAM without interruptions.

---

### Links
- Gpt4All: https://gpt4all.io/
- mcp-use: https://pypi.org/project/mcp-use/#quick-start
- fastmcp for Zapier: https://pypi.org/project/fastmcp/
- Docker MCP-Toolkit: https://hub.docker.com/search?q=mcp+toolkit
- langchain docs: https://python.langchain.com/docs/integrations/providers/gpt4all/
- langchain docs: https://python.langchain.com/api_reference/community/llms/langchain_community.llms.gpt4all.GPT4All.html
- LLM: https://ollama.com/MFDoom/deepseek-r1-tool-calling?utm_source=chatgpt.com
- Start LLMs locally: https://ollama.com/
- mcp-use docs: https://docs.mcp-use.io/essentials/agent-configuration
- bind_tools: https://github.com/langchain-ai/langchain/discussions/21907
- Claude bind_tools: https://github.com/anthropics/anthropic-tools/blob/main/tool_use_package/EXAMPLES.md?utm_source=chatgpt.com
- more bind_tools infos: https://github.com/langchain-ai/langchain/discussions/25811?utm_source=chatgpt.com

---

### Infos
- ollama to start 
- llama3 does not support bind_tools
- ollama create deepseek-lite -f Modelfile - The standard deepseek model took too much power therefore I changed the parameters with the aid of the Modelfile.

### Tool Implementation
- OpenAi: https://platform.openai.com/docs/guides/function-calling?api-mode=responses&example=get-weather
- Claude tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview