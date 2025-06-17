from pydantic import BaseModel
from lib.model.model import load_model
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
import json
from dotenv import load_dotenv
import os
load_dotenv()
model = load_model()

class PromptRequest(BaseModel):
    prompt: str
    
MCP_URL = os.getenv("MCP_ZAPIER_URL")
transport = StreamableHttpTransport(MCP_URL)
client = Client(transport=transport)

def generate_response(prompt: str) -> str:
    response = model.generate(prompt, max_tokens=1000)
    print(f"Prompt: {prompt}")
    print(f"Response: {response}")
    return response

async def send_email_via_mcp(body: str):
    email = os.getenv("EMAIL")
    async with client:
        result = await client.call_tool(
            "gmail_send_email",
            {
                "to": email,
                "subject": "Plant Watering Reminder",
                "body": body,
                "instructions": "Send an email with the provided body.",
            },
        )
        return json.loads(result[0].text)