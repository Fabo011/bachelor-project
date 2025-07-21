# Streamlit-App

## Installation

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

```
brew install ollama
ollama pull llama3
```

If you want to use deepseek LLM
```
ollama pull MFDoom/deepseek-v2-tool-calling:latest
ollama create deepseek-lite -f Modelfile
```

Delete models which are no longer needed
```
ollama rm <model-name>
```

**Start Server**
```
ollama serve
streamlit run app.py
```
---

### Ollama
A local model server + CLI for running and managing open-source LLMs (LLaMA, DeepSeek, Mistral, etc.).

---

### MCP
Ollama tools calls the connected mcp servers based on the prompt.

---

### Modelfile
Configurations for the LLM. Llama3 was running without adjustments. I`ve changed the parameters for deepseek to run it on Synology NAS (CPU) without interruptions.

---

### Links
- fastmcp for Zapier: https://pypi.org/project/fastmcp/
- Docker MCP-Toolkit: https://hub.docker.com/search?q=mcp+toolkit
- LLM: https://ollama.com/MFDoom/deepseek-r1-tool-calling?utm_source=chatgpt.com
- Start LLMs locally: https://ollama.com/
- Ollama models with tool capabilities: https://ollama.com/search?c=tools

---

### Tool Implementation Links
- Ollama: https://ollama.com/blog/tool-support
- OpenAi Function Calling: https://platform.openai.com/docs/guides/function-calling?api-mode=responses&example=get-weather
- Claude tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview

---

### Running Prompts without using Pre-Prompts 
**Running prompt for mails: CallTool:** Send an email to myemail@proton.me with subject "Meeting Follow-up" and body "Hi Alice, thanks for the great meeting today. Let's catch up next week." with the gmail_send_email tool Instructions: send it ASAP.


**Running prompt for duckduckgo search:** callTool Use MCP_DOCKER_search to look up "the best austrian meals for dinner". Return 5 results with safeSearch=off.

**Running prompt for duckduckgo fetch_content:** callTool Use MCP_DOCKER_fetch_content to fetch the text contents of this homepage: https://yourdomain.com

**Running prompt for wikipedia get_summary:** calltool Please give me a summary about a wikipedia article of nikolas tesla with the wikipedia tool MCP_DOCKER_get_summary

**Info:** If you want to talk with the llm without tool, just ask questions without "calltool".


### Running Prompts with Pre-Prompts
**Exact definitions of the tool names no longer required, the llm learned the tools by the pre prompt.**

**Running prompt for duckduckgo fetch_content:** callTool Use duckduchgo fetch tool to fetch the text contents of this homepage: https://yourdomain.com

**Running prompt for wikipedia get_summary:** calltool Please give me a summary about a wikipedia article of michael schumacher with the wikipedia tool get summary

---

### How to Dockerize whole Infrastructure
1. Start ollama in docker: https://hub.docker.com/r/ollama/ollama
2. Start MCP-Servers in docker: 
   - Github: https://hub.docker.com/r/mcp/github-mcp-server
   - duckduckgo: https://hub.docker.com/r/mcp/duckduckgo
   - elasticsearch: https://hub.docker.com/r/mcp/elasticsearch
3. Build streamlit app docker container
4. Run the containers:
   - locally: e.g. Synology NAS or on computers (mac, linux). Consider Watchtower to automatically update docker container: https://containrrr.dev/watchtower/
   - cloud: e.g. Azure Container Apps: Azure Container Apps is a serverless platform that allows you to run containerized applications without managing infrastructure. It supports features like automatic scaling, event-driven processing, and easy deployment of microservices. For ollama I propose to use serverless GPU: https://learn.microsoft.com/en-us/azure/container-apps/gpu-serverless-overview

---

### MCP Toolhub API
To avoid redefining each tool from scratch in every project, I created the mcp-toolhub-api https://github.com/Fabo011/mcp-toolhub-api. 
This API can be expanded and enhanced by the community in the future. See readme in https://github.com/Fabo011/mcp-toolhub-api.

---

### Impressions from Testing

Create Github Issue with Github MCP-Server
<img width="1573" height="935" alt="create-github-issue" src="https://github.com/user-attachments/assets/792596d3-a468-4728-ab34-f456b6161d78" />

Serach with DuckDuckGo MCP-Server
<img width="1525" height="925" alt="duckduckgosearch" src="https://github.com/user-attachments/assets/9c912ce1-b09e-484d-9fbc-5ca131031730" />

Send email with Zapier MCP-Server
<img width="1556" height="935" alt="send-email" src="https://github.com/user-attachments/assets/d4980572-612c-4956-ba05-7c5ab99736b9" />

Get summary from a Wikipedia-Page with Wikipedia MCP-Server
<img width="1497" height="936" alt="wikipedia-get-summary" src="https://github.com/user-attachments/assets/e1c1464d-0ee6-4479-ae57-d33f61694aaf" />

