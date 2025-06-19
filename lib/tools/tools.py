create_issue_tool = {
    "type": "function",
    "function": {
        "name": "create_issue",
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

# e.g. another_tool = { ... }
