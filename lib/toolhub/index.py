import httpx  # better than requests for async

async def fetch_tools_from_toolhub():
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get("http://127.0.0.1:9000/tools")
            res.raise_for_status()
            data = res.json()
            return data.get("tools", []), data.get("prompts", {})
    except Exception as e:
        print(f"Failed to load tools from ToolHub API: {e}")
        return [], {}
