import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

import ollama
import streamlit as st
from fastmcp import Client

from lib.tools.tools import duckduckgo_fetch_content_tool, duckduckgo_search_tool

# -------------------------
# CONFIGURATION
# -------------------------

HISTORY_DIR = Path("conversation_history")
MAX_AGENT_ITERATIONS = 3
MODEL_NAME = "llama3.1"

# -------------------------
# FILE OPERATIONS
# -------------------------

def ensure_history_directory():
    """Create history directory if it doesn't exist"""
    HISTORY_DIR.mkdir(exist_ok=True)


def get_user_history_file(username: str) -> Path:
    """Get the path to user's conversation history file"""
    safe_username = "".join(c for c in username if c.isalnum() or c in ('-', '_'))
    return HISTORY_DIR / f"{safe_username}_history.json"


def save_conversation_history(username: str, messages: List[Dict]):
    """
    Save conversation history to a JSON file.
    
    Args:
        username: User's name
        messages: List of message dictionaries
    """
    ensure_history_directory()
    history_file = get_user_history_file(username)
    
    history_data = {
        "username": username,
        "last_updated": datetime.now().isoformat(),
        "messages": messages
    }
    
    try:
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved conversation history for {username}")
    except Exception as e:
        print(f"❌ Error saving history: {e}")


def load_conversation_history(username: str) -> List[Dict]:
    """
    Load conversation history from a JSON file.
    
    Args:
        username: User's name
    
    Returns:
        List of message dictionaries, or default welcome message if not found
    """
    history_file = get_user_history_file(username)
    
    if not history_file.exists():
        print(f"📂 No history found for {username}, starting fresh")
        return [{"role": "assistant", "content": f"Hi {username}! I'm an AI agent. Ask me anything, and I'll autonomously decide if I need to use tools to help answer your question!"}]
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
        
        messages = history_data.get("messages", [])
        last_updated = history_data.get("last_updated", "unknown")
        print(f"📂 Loaded {len(messages)} messages for {username} (last updated: {last_updated})")
        return messages
    except Exception as e:
        print(f"❌ Error loading history: {e}")
        return [{"role": "assistant", "content": f"Hi {username}! I'm an AI agent. Ask me anything!"}]


def clear_conversation_history(username: str):
    """
    Clear conversation history for a user.
    
    Args:
        username: User's name
    """
    history_file = get_user_history_file(username)
    
    if history_file.exists():
        try:
            history_file.unlink()
            print(f"🗑️ Cleared conversation history for {username}")
            return True
        except Exception as e:
            print(f"❌ Error clearing history: {e}")
            return False
    return True


def list_all_users() -> List[str]:
    """
    List all users with saved conversation history.
    
    Returns:
        List of usernames
    """
    ensure_history_directory()
    users = []
    
    for file in HISTORY_DIR.glob("*_history.json"):
        username = file.stem.replace("_history", "")
        users.append(username)
    
    return sorted(users)

# -------------------------
# MCP CLIENT INITIALIZATION
# -------------------------

# -------------------------
# MCP CLIENT INITIALIZATION
# -------------------------

@st.cache_resource
def init_mcp_client():
    """Initialize MCP client once and cache it"""
    with open("mcp.json", "r") as f:
        config = json.load(f)
    
    client = Client(config)
    
    # Run async initialization in a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(client.__aenter__())
        tools = loop.run_until_complete(client.list_tools())
        print("🔧 Available tools from MCP server:")
        for tool in tools:
            print(f"- {tool.name}")
    finally:
        # Keep the loop for future calls
        pass
    
    return client, loop


# Initialize MCP client
mcp_client, event_loop = init_mcp_client()

# -------------------------
# AGENT FUNCTIONS
# -------------------------

def execute_tool_call(tool_name: str, args: Dict) -> Tuple[str, bool]:
    """
    Execute a single tool call.
    
    Args:
        tool_name: Name of the tool to call
        args: Arguments for the tool
    
    Returns:
        Tuple of (result_text, success_flag)
    """
    try:
        result = event_loop.run_until_complete(
            mcp_client.call_tool(tool_name, args)
        )
        
        if hasattr(result, 'content') and result.content:
            raw_text = "\n".join([item.text for item in result.content if hasattr(item, 'text')])
        else:
            raw_text = str(result)
        
        if not raw_text:
            raw_text = "⚠️ Tool returned no result"
        
        return raw_text, True
    except Exception as tool_error:
        error_msg = f"⚠️ Tool error: {str(tool_error)}"
        return error_msg, False


def run_agent(user_prompt: str, max_iterations: int = MAX_AGENT_ITERATIONS) -> Tuple[str, List[str]]:
    """
    Simple agent that can reason and use tools autonomously.
    
    Args:
        user_prompt: The user's question
        max_iterations: Maximum number of tool-use iterations
    
    Returns:
        tuple: (final_response, agent_steps)
    """
    agent_steps = []
    conversation_history = [{"role": "user", "content": user_prompt}]
    
    for iteration in range(max_iterations):
        agent_steps.append(f"**🤖 Agent Iteration {iteration + 1}**")
        
        # Agent always has access to tools
        response = ollama.chat(
            model=MODEL_NAME,
            messages=conversation_history,
            tools=[duckduckgo_search_tool, duckduckgo_fetch_content_tool]
        )
        
        assistant_message = response.get("message", {})
        llm_message = assistant_message.get("content", "").strip()
        tool_calls = assistant_message.get("tool_calls", [])
        
        # Agent is thinking
        if llm_message:
            agent_steps.append(f"💭 *Agent thinking: {llm_message}*")
        
        # No tool calls? Agent has finished reasoning
        if not tool_calls:
            agent_steps.append("✅ *Agent finished - no more tools needed*")
            return llm_message, agent_steps
        
        # Agent decided to use tools
        agent_steps.append(f"🔧 *Agent using {len(tool_calls)} tool(s)*")
        
        # Execute all tool calls
        tool_results_text = []
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]
            
            agent_steps.append(f"  → Calling `{tool_name}` with args: `{args}`")
            
            result_text, success = execute_tool_call(tool_name, args)
            tool_results_text.append(f"Tool {tool_name} result:\n{result_text}")
            
            if success:
                agent_steps.append(f"  ✓ Tool returned {len(result_text)} characters")
            else:
                agent_steps.append(f"  ✗ Tool error occurred")
        
        # Add assistant message and tool results to conversation history
        conversation_history.append(assistant_message)
        conversation_history.append({
            "role": "tool",
            "content": "\n\n".join(tool_results_text)
        })
        
        agent_steps.append("")
    
    # Max iterations reached
    agent_steps.append("⚠️ *Agent reached maximum iterations*")
    
    # Get final answer from agent
    conversation_history.append({
        "role": "user", 
        "content": "Based on the tool results, please provide your final answer."
    })
    
    final_response = ollama.chat(
        model=MODEL_NAME,
        messages=conversation_history
    )
    
    final_answer = final_response.get("message", {}).get("content", "").strip()
    return final_answer, agent_steps


def format_agent_response(agent_steps: List[str], final_answer: str) -> str:
    """
    Format the agent's response for display.
    
    Args:
        agent_steps: List of agent step descriptions
        final_answer: The final answer from the agent
    
    Returns:
        Formatted response string
    """
    response = "### 🤖 Agent Process\n\n"
    response += "\n".join(agent_steps)
    response += "\n\n---\n\n"
    response += "### 📝 Final Answer\n\n"
    response += final_answer
    return response


def display_message_with_animation(placeholder, message: str, delay: float = 0.01):
    """
    Display a message with typing animation.
    
    Args:
        placeholder: Streamlit placeholder object
        message: Message to display
        delay: Delay between words in seconds
    """
    display = ""
    for word in message.split():
        display += word + " "
        placeholder.markdown(display + "▌")
        time.sleep(delay)
    placeholder.markdown(display)

# -------------------------
# STREAMLIT UI
# -------------------------

st.set_page_config(page_title="AI Agent with MCP Tools", layout="centered")
st.title("� AI Agent with MCP Tools")

# Add agent explanation in sidebar
with st.sidebar:
    st.header("ℹ️ How This Agent Works")
    st.markdown("""
    This is a **simple autonomous agent** that:
    
    1. �🧠 **Reasons** about your question
    2. 🎯 **Plans** what tools to use
    3. 🔧 **Uses tools** automatically (no keywords needed!)
    4. 🔄 **Iterates** - can use multiple tools in sequence
    5. 📝 **Synthesizes** a final answer
    
    Just ask a question naturally and watch the agent work!
    
    **Max iterations:** 3  
    **Available tools:** DuckDuckGo Search, DuckDuckGo Fetch Content
    """)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm an AI agent. Ask me anything, and I'll autonomously decide if I need to use tools to help answer your question!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def run_agent(user_prompt: str, max_iterations: int = 3):
    """
    Simple agent that can reason and use tools autonomously.
    
    Args:
        user_prompt: The user's question
        max_iterations: Maximum number of tool-use iterations
    
    Returns:
        tuple: (final_response, agent_steps)
    """
    agent_steps = []
    conversation_history = [{"role": "user", "content": user_prompt}]
    
    for iteration in range(max_iterations):
        agent_steps.append(f"**🤖 Agent Iteration {iteration + 1}**")
        
        # Agent always has access to tools
        response = ollama.chat(
            model="llama3.1",
            messages=conversation_history,
            tools=[duckduckgo_search_tool, duckduckgo_fetch_content_tool]
        )
        
        assistant_message = response.get("message", {})
        llm_message = assistant_message.get("content", "").strip()
        tool_calls = assistant_message.get("tool_calls", [])
        
        # Agent is thinking
        if llm_message:
            agent_steps.append(f"💭 *Agent thinking: {llm_message}*")
        
        # No tool calls? Agent has finished reasoning
        if not tool_calls:
            agent_steps.append("✅ *Agent finished - no more tools needed*")
            return llm_message, agent_steps
        
        # Agent decided to use tools
        agent_steps.append(f"🔧 *Agent using {len(tool_calls)} tool(s)*")
        
        # Execute all tool calls
        tool_results_text = []
        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]
            
            agent_steps.append(f"  → Calling `{tool_name}` with args: `{args}`")
            
            try:
                result = event_loop.run_until_complete(
                    mcp_client.call_tool(tool_name, args)
                )
                
                if hasattr(result, 'content') and result.content:
                    raw_text = "\n".join([item.text for item in result.content if hasattr(item, 'text')])
                else:
                    raw_text = str(result)
                
                if not raw_text:
                    raw_text = "⚠️ Tool returned no result"
                
                tool_results_text.append(f"Tool {tool_name} result:\n{raw_text}")
                agent_steps.append(f"  ✓ Tool returned {len(raw_text)} characters")
                
            except Exception as tool_error:
                error_msg = f"⚠️ Tool error: {str(tool_error)}"
                tool_results_text.append(f"Tool {tool_name} error:\n{error_msg}")
                agent_steps.append(f"  ✗ Tool error: {tool_error}")
        
        # Add assistant message and tool results to conversation history
        conversation_history.append(assistant_message)
        conversation_history.append({
            "role": "tool",
            "content": "\n\n".join(tool_results_text)
        })
        
        agent_steps.append("")
    
    # Max iterations reached
    agent_steps.append("⚠️ *Agent reached maximum iterations*")
    
    # Get final answer from agent
    conversation_history.append({
        "role": "user", 
        "content": "Based on the tool results, please provide your final answer."
    })
    
    final_response = ollama.chat(
        model="llama3.1",
        messages=conversation_history
    )
    
    final_answer = final_response.get("message", {}).get("content", "").strip()
    return final_answer, agent_steps


if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Run the agent!
            final_answer, agent_steps = run_agent(prompt, max_iterations=3)
            
            # Show agent's reasoning process
            full_response = "### 🤖 Agent Process\n\n"
            full_response += "\n".join(agent_steps)
            full_response += "\n\n---\n\n"
            full_response += "### 📝 Final Answer\n\n"
            full_response += final_answer

            # Final fallback - ensure there's always something to display
            if not full_response or full_response.strip() == "":
                full_response = "_No response from agent._"

        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            full_response = f"**⚠️ Error occurred:**\n```\n{str(e)}\n```\n\n**Details:**\n```\n{error_details}\n```"
            print(f"❌ Error: {error_details}")

        # Typing animation
        display = ""
        for word in full_response.split():
            display += word + " "
            placeholder.markdown(display + "▌")
            time.sleep(0.01)
        placeholder.markdown(display)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
