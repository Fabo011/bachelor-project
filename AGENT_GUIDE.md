# 🤖 Simple AI Agent Guide

## What is an Agent?

An **AI Agent** is different from a simple chatbot. Instead of just responding to prompts, an agent can:

- **🧠 Think** - Reason about what needs to be done
- **🎯 Plan** - Decide which tools to use and when
- **🔧 Act** - Execute tools autonomously
- **🔄 Iterate** - Use multiple tools in sequence, learning from each result
- **📝 Reflect** - Synthesize information into a final answer

## How This Simple Agent Works

### The Agent Loop

```
User Question
    ↓
┌───────────────────────────────┐
│  Agent Iteration 1            │
│  1. Reason about the question │
│  2. Decide: Need tools?       │
│  3. If yes → Call tool(s)     │
│  4. Get results               │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│  Agent Iteration 2            │
│  1. Review tool results       │
│  2. Decide: Need more tools?  │
│  3. If yes → Call more tools  │
│  4. Get more results          │
└───────────────────────────────┘
    ↓
┌───────────────────────────────┐
│  Agent Iteration 3            │
│  1. Review all results        │
│  2. Synthesize final answer   │
│  3. Return to user            │
└───────────────────────────────┘
```

### Key Differences from Simple Chat

| Feature | Simple Chat | Agent |
|---------|-------------|-------|
| Tool use | Manual (keyword trigger) | Autonomous |
| Planning | None | Multi-step reasoning |
| Iteration | Single response | Multiple rounds |
| Context | Loses tool results | Maintains conversation |
| Decision making | None | Decides what tools to use |

## Code Walkthrough

### 1. Agent Function (`run_agent`)

```python
def run_agent(user_prompt: str, max_iterations: int = 3):
```

This is the brain of the agent. It:
- Takes a user prompt
- Runs up to 3 iterations (configurable)
- Returns the final answer and reasoning steps

### 2. Conversation History

```python
conversation_history = [{"role": "user", "content": user_prompt}]
```

The agent maintains a **conversation history** that includes:
- User messages
- Assistant (LLM) messages
- Tool results

This is crucial! The LLM can see what tools were used and their results.

### 3. The Agent Loop

```python
for iteration in range(max_iterations):
```

Each iteration:
1. **Calls the LLM** with conversation history + available tools
2. **Checks if LLM wants to use tools** (via `tool_calls`)
3. **Executes tools** if requested
4. **Adds results** to conversation history
5. **Repeats** until LLM decides it has enough information

### 4. Tool Execution

```python
result = event_loop.run_until_complete(
    mcp_client.call_tool(tool_name, args)
)
```

When the LLM decides to use a tool:
- The agent extracts tool name and arguments
- Calls the MCP tool
- Gets results
- Adds to conversation history

### 5. Termination Conditions

The agent stops when:
- **No tool calls**: LLM decides it has enough information
- **Max iterations**: Safety limit reached (prevents infinite loops)

## Example Agent Execution

**User:** "What are the best restaurants in Austria?"

```
🤖 Agent Iteration 1
💭 Agent thinking: I need to search for information...
🔧 Agent using 1 tool(s)
  → Calling `search` with args: `{"query": "best restaurants in Austria"}`
  ✓ Tool returned 5432 characters

🤖 Agent Iteration 2
💭 Agent thinking: I have search results, let me fetch details...
🔧 Agent using 1 tool(s)
  → Calling `fetch_content` with args: `{"url": "https://..."}`
  ✓ Tool returned 8234 characters

🤖 Agent Iteration 3
✅ Agent finished - no more tools needed

📝 Final Answer:
Based on my research, here are the top restaurants in Austria:
1. [Restaurant name and details]
2. [Restaurant name and details]
...
```

## Making It More Advanced

Want to enhance this agent? Here are ideas:

### 1. **ReAct Pattern** (Reason + Act)
Add explicit reasoning steps:
```python
# After each tool use:
conversation_history.append({
    "role": "user",
    "content": "Observation: [tool result]. What should we do next?"
})
```

### 2. **Memory**
Store conversation across sessions:
```python
if "agent_memory" not in st.session_state:
    st.session_state.agent_memory = []
```

### 3. **More Tools**
Add more capabilities:
- Web scraping
- Calculator
- Database queries
- API calls
- File operations

### 4. **Planning Phase**
Add explicit planning before acting:
```python
# First call: Make a plan
plan = llm.chat("Create a step-by-step plan to answer: {question}")
# Then execute the plan
```

### 5. **Self-Reflection**
Let agent critique its own answers:
```python
critique = llm.chat("Is this answer complete and accurate? What's missing?")
```

## Key Takeaways

1. **Agents loop** - They don't just respond once
2. **Agents maintain context** - Conversation history is crucial
3. **Agents decide** - They choose when and which tools to use
4. **Agents iterate** - They can use multiple tools in sequence
5. **Agents are autonomous** - No manual triggers needed

## Run the Agent

```bash
uv run streamlit run app.py
```

Then just ask natural questions - no special keywords needed! The agent will autonomously decide if it needs tools.

## Learn More

- **ReAct Paper**: "ReAct: Synergizing Reasoning and Acting in Language Models"
- **Tool Use**: How LLMs call external functions
- **Agent Frameworks**: LangChain, AutoGPT, BabyAGI
- **MCP**: Model Context Protocol for tool integration

---

🎉 **Congratulations!** You now understand how AI agents work at a fundamental level!
