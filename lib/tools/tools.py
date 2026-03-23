duckduckgo_search_tool = {
    "type": "function",
    "function": {
        "name": "search",
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
        "name": "fetch_content",
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
