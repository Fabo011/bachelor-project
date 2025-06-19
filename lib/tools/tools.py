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
