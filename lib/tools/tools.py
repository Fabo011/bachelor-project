create_issue_tool = {
    "type": "function",
    "function": {
        "name": "MCP_DOCKER_create_issue",
        "description": "Create a GitHub issue using the connected MCP server",
        "parameters": {
            "type": "object",
            "properties": {
                "owner": {
                    "type": "string",
                    "description": "Owner or organization of the GitHub repository"
                },
                "repo": {
                    "type": "string",
                    "description": "Name of the GitHub repository"
                },
                "title": {
                    "type": "string",
                    "description": "Title of the issue"
                },
                "body": {
                    "type": "string",
                    "description": "Body/description of the issue"
                },
            },
            "required": ["owner", "repo", "title", "body"]
        }
    }
}

gmail_send_email_tool = {
    "type": "function",
    "function": {
        "name": "Zapier_gmail_send_email",
        "description": "Send an email using the Zapier MCP gmail_send_email tool",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address"},
                "subject": {"type": "string", "description": "Subject of the email"},
                "body": {"type": "string", "description": "Body content of the email"},
                "instructions": {"type": "string", "description": "Optional instructions for sending the email"},
            },
            "required": ["to", "subject", "body"]
        }
    }
}

duckduckgo_search_tool = {
    "type": "function",
    "function": {
        "name": "MCP_DOCKER_search",
        "description": "Search the web using DuckDuckGo via the MCP server with the tool search.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string (max 400 characters)"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of results to return (1–20, default: 10)"
                },
                "safeSearch": {
                    "type": "string",
                    "description": "Safety level: strict, moderate, or off (default: moderate)",
                    "enum": ["strict", "moderate", "off"]
                }
            },
            "required": ["query"]
        }
    }
}

duckduckgo_fetch_content_tool = {
    "type": "function",
    "function": {
        "name": "MCP_DOCKER_fetch_content",
        "description": "Fetch the content of a web page from a given URL using DuckDuckGo's fetch_content tool.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the page to fetch content from"
                },
                "maxTokens": {
                    "type": "integer",
                    "description": "Maximum number of tokens to return (optional, default is 1000)"
                }
            },
            "required": ["url"]
        }
    }
}

wikipedia_get_summary_tool = {
    "type": "function",
    "function": {
        "name": "MCP_DOCKER_get_summary",
        "description": "Get a summary of a Wikipedia page for a given topic or title with the tool get_summary.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the Wikipedia page to summarize"
                },
                "sentences": {
                    "type": "integer",
                    "description": "Number of sentences to include in the summary (optional)"
                }
            },
            "required": ["title"]
        }
    }
}
