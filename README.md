# AI Workflow

## Installation

Disclaimer: This is made and tested on Apple M1 with 16gb RAM.

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
ollama serve
streamlit run app.py
```
---

### Ollama
A local model server + CLI for running and managing open-source LLMs (LLaMA, Mistral, etc.).

---

### MCP
Ollama tools calls the connected mcp servers based on the prompt.

---

### Modelfile
Configurations for the LLM. llama3 was running without adjustments. I`ve changed the parameters for deepseek to run it on Mac M1 with 16gb RAM without interruptions.

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
- OpenAi: https://platform.openai.com/docs/guides/function-calling?api-mode=responses&example=get-weather
- Claude tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview

---

### Prompt
**Hint:** Use thunderclient extention in VsCode.

What’s the best place to visit in Málaga? Please include a short answer in your reply. Then, create a GitHub issue titled 'Book a flight to Málaga' in the 'repo-name' repository with the right tool. Also, send an email to myemail@proton.me with the right tool containing your answer about the best place to visit.

### Response from LLM
```
{
  "llm_response": [
    {
      "tool": "Zapier_gmail_send_email",
      "result": {
        "results": [
          {
            "id": "197878948989893434d0237",
            "threadId": "197878948989893434d0237",
            "labelIds": [
              "SENT"
            ]
          }
        ],
        "feedbackUrl": "https://mcp.zapier.com/mcp/servers/id/history/executions/id",
        "execution": {
          "id": "789jfhuig8989343b4j4i39",
          "actionId": "8c503190-fe13-45d3-a89b-29494e1ed8e3",
          "mcpServerId": "a2748489-8700-4b85-b542-538fa712f517",
          "instructions": "",
          "params": {
            "to": "<myemail>@proton.me",
            "body": "One of the best places to visit in Málaga is the historic center, which features stunning architecture and rich history.",
            "subject": "Best Place to Visit in Málaga",
            "instructions": ""
          },
          "resolvedParams": {
            "to": {
              "name": "To",
              "label": null,
              "value": "<myemail>@proton.me",
              "reason": "top-level-hint",
              "status": "locked"
            },
            "body": {
              "name": "Body",
              "label": null,
              "value": "One of the best places to visit in Málaga is the historic center, which features stunning architecture and rich history.",
              "reason": "top-level-hint",
              "status": "locked"
            },
            "subject": {
              "name": "Subject",
              "label": null,
              "value": "Best Place to Visit in Málaga",
              "reason": "top-level-hint",
              "status": "locked"
            }
          },
          "status": "SUCCESS",
          "createdDT": "2025-06-19T09:34:33.638Z"
        },
        "isPreview": false
      }
    },
    {
      "tool": "MCP_DOCKER_create_issue",
      "result": {
        "id": 3159655169,
        "number": 35,
        "state": "open",
        "locked": false,
        "title": "Book a flight to M?laga",
        "body": "Please book a flight to M?laga for further instructions.",
        "author_association": "OWNER",
        "user": {
          "login": "Fabo011",
          "id": 93132701,
          "node_id": "U_kgDOBY0XnQ",
          "avatar_url": "https://avatars.githubusercontent.com/u/93132701?v=4",
          "html_url": "https://github.com/Fabo011",
          "gravatar_id": "",
          "type": "User",
          "site_admin": false,
          "url": "https://api.github.com/users/Fabo011",
          "events_url": "https://api.github.com/users/Fabo011/events{/privacy}",
          "following_url": "https://api.github.com/users/Fabo011/following{/other_user}",
          "followers_url": "https://api.github.com/users/Fabo011/followers",
          "gists_url": "https://api.github.com/users/Fabo011/gists{/gist_id}",
          "organizations_url": "https://api.github.com/users/Fabo011/orgs",
          "received_events_url": "https://api.github.com/users/Fabo011/received_events",
          "repos_url": "https://api.github.com/users/Fabo011/repos",
          "starred_url": "https://api.github.com/users/Fabo011/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/Fabo011/subscriptions"
        },
        "comments": 0,
        "created_at": "2025-06-19T09:34:34Z",
        "updated_at": "2025-06-19T09:34:34Z",
        "url": "https://api.github.com/repos/Fabo011/bachelor-project/issues/35",
        "html_url": "https://github.com/Fabo011/bachelor-project/issues/35",
        "comments_url": "https://api.github.com/repos/Fabo011/bachelor-project/issues/35/comments",
        "events_url": "https://api.github.com/repos/Fabo011/bachelor-project/issues/35/events",
        "labels_url": "https://api.github.com/repos/Fabo011/bachelor-project/issues/35/labels{/name}",
        "repository_url": "https://api.github.com/repos/Fabo011/bachelor-project",
        "reactions": {
          "total_count": 0,
          "+1": 0,
          "-1": 0,
          "laugh": 0,
          "confused": 0,
          "heart": 0,
          "hooray": 0,
          "rocket": 0,
          "eyes": 0,
          "url": "https://api.github.com/repos/Fabo011/bachelor-project/issues/35/reactions"
        },
        "node_id": "I_kwDOO3nuSM68VZZUIMB"
      }
    }
  ]
}
```