# 🤖 AI Agent with Persistent Conversation History

## ✨ New Features

### 1. **User-Based Conversation History** 💾
- Each user has their own persistent conversation history
- Conversations are saved automatically after each message
- History is stored in JSON files in the `conversation_history/` directory
- Resume your conversation anytime, even after restarting the server!

### 2. **User Authentication** 👤
- Simple login screen where users enter their name
- Shows existing users on the login page
- Each user gets a personalized greeting

### 3. **History Management** 🗑️
- **Logout**: Save your conversation and logout
- **Clear History**: Start fresh while staying logged in
- User information displayed in sidebar

### 4. **Refactored Code Structure** 🏗️
The code is now organized into clear, maintainable sections:

```python
# File Operations
- ensure_history_directory()
- get_user_history_file(username)
- save_conversation_history(username, messages)
- load_conversation_history(username)
- clear_conversation_history(username)
- list_all_users()

# MCP Client
- init_mcp_client()

# Agent Functions
- execute_tool_call(tool_name, args)
- run_agent(user_prompt, max_iterations)
- format_agent_response(agent_steps, final_answer)
- display_message_with_animation(placeholder, message, delay)

# UI Sections
- User Authentication
- Main Chat Interface
```

## 📂 File Structure

```
conversation_history/
├── John_history.json
├── Alice_history.json
└── Bob_history.json
```

### Example History File (`John_history.json`):

```json
{
  "username": "John",
  "last_updated": "2026-03-23T14:30:45.123456",
  "messages": [
    {
      "role": "assistant",
      "content": "Hi John! I'm an AI agent..."
    },
    {
      "role": "user",
      "content": "What are the best restaurants in Austria?"
    },
    {
      "role": "assistant",
      "content": "### 🤖 Agent Process\n\n..."
    }
  ]
}
```

## 🚀 Usage

### 1. Start the App

```bash
uv run streamlit run app.py
```

### 2. Login

- Enter your name on the login screen
- Click "Start Chat"
- If you've used the app before, your conversation will be loaded

### 3. Chat

- Ask questions naturally
- The agent will autonomously use tools
- Your conversation is saved automatically

### 4. Manage Your Session

**Sidebar options:**
- **Logout**: Saves your conversation and returns to login
- **Clear History**: Deletes your history and starts fresh

## 🔧 Configuration

Edit these constants in `app.py`:

```python
HISTORY_DIR = Path("conversation_history")  # Where histories are saved
MAX_AGENT_ITERATIONS = 3                     # Max tool iterations
MODEL_NAME = "llama3.1"                      # Ollama model to use
```

## 📊 Benefits of the New Structure

### ✅ Better Maintainability
- Each function has a single, clear responsibility
- Easy to find and modify specific functionality
- Well-documented with docstrings

### ✅ Better Testability
- Functions can be tested independently
- Clear inputs and outputs
- Separated business logic from UI

### ✅ Better Extensibility
- Easy to add new features (e.g., export history, search history)
- Easy to add new authentication methods
- Easy to add new storage backends (database, cloud storage)

## 🎯 Function Overview

### File Operations

| Function | Purpose | Parameters | Returns |
|----------|---------|------------|---------|
| `ensure_history_directory()` | Creates history directory | None | None |
| `get_user_history_file()` | Gets path to user's file | `username: str` | `Path` |
| `save_conversation_history()` | Saves conversation | `username, messages` | None |
| `load_conversation_history()` | Loads conversation | `username: str` | `List[Dict]` |
| `clear_conversation_history()` | Deletes history | `username: str` | `bool` |
| `list_all_users()` | Lists all users | None | `List[str]` |

### Agent Functions

| Function | Purpose | Parameters | Returns |
|----------|---------|------------|---------|
| `execute_tool_call()` | Executes a single tool | `tool_name, args` | `(str, bool)` |
| `run_agent()` | Runs the agent loop | `user_prompt, max_iterations` | `(str, List[str])` |
| `format_agent_response()` | Formats response | `agent_steps, final_answer` | `str` |
| `display_message_with_animation()` | Shows typing effect | `placeholder, message, delay` | None |

## 🔒 Security Notes

### Current Implementation (Proof of Concept)
- ⚠️ No password authentication
- ⚠️ No encryption of conversation data
- ⚠️ No user verification

### For Production Use, Consider Adding:
- 🔐 Password/OAuth authentication
- 🔐 Encrypted storage
- 🔐 Session management with timeouts
- 🔐 Rate limiting
- 🔐 User roles and permissions
- 🔐 GDPR compliance (data export, deletion rights)

## 💡 Future Enhancements

### Potential Features to Add:

1. **Export Conversations**
   ```python
   def export_conversation_to_markdown(username: str) -> str:
       """Export conversation as markdown file"""
   ```

2. **Search History**
   ```python
   def search_conversation(username: str, query: str) -> List[Dict]:
       """Search through conversation history"""
   ```

3. **Conversation Analytics**
   ```python
   def get_conversation_stats(username: str) -> Dict:
       """Get stats: message count, tool usage, etc."""
   ```

4. **Multiple Conversations per User**
   ```python
   def create_conversation(username: str, title: str) -> str:
       """Create a new conversation thread"""
   ```

5. **Conversation Sharing**
   ```python
   def share_conversation(username: str, conv_id: str) -> str:
       """Generate shareable link"""
   ```

## 🧪 Testing

### Test the File Operations:

```python
# Create a test user
save_conversation_history("TestUser", [{"role": "user", "content": "Hello"}])

# Load the history
messages = load_conversation_history("TestUser")
assert len(messages) == 1

# Clear the history
clear_conversation_history("TestUser")

# Verify it's cleared
history_file = get_user_history_file("TestUser")
assert not history_file.exists()
```

## 📖 Code Quality Improvements

### Before (Monolithic):
```python
# Everything in one place, hard to maintain
if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append(...)
    # ... lots of code ...
```

### After (Modular):
```python
# Clear separation of concerns
if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    final_answer, agent_steps = run_agent(prompt)
    full_response = format_agent_response(agent_steps, final_answer)
    display_message_with_animation(placeholder, full_response)
    
    save_conversation_history(st.session_state.username, st.session_state.messages)
```

## 🎓 Learning Points

### What You've Learned:

1. ✅ **Persistent Storage**: Saving and loading data from files
2. ✅ **User Management**: Simple user-based data separation
3. ✅ **Code Organization**: Breaking monolithic code into maintainable functions
4. ✅ **Error Handling**: Graceful handling of file operations
5. ✅ **State Management**: Using Streamlit session state effectively

### Key Software Engineering Principles Applied:

- **Single Responsibility Principle**: Each function does one thing well
- **Separation of Concerns**: UI, business logic, and data are separated
- **DRY (Don't Repeat Yourself)**: Reusable functions
- **Clear Naming**: Function names explain what they do
- **Documentation**: Comprehensive docstrings

---

🎉 **Enjoy your improved AI Agent with persistent conversation history!**
