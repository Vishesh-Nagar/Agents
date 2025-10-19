# Agent Team Weather Assistant

This project implements a multi-agent weather assistant system using Google ADK (Agent Development Kit). The system features a team of specialized agents that handle weather queries, greetings, farewells, and includes guardrails for input and tool usage.

## Project Structure

The monolithic code has been refactored into modular components for better maintainability and scalability:

```
agent_team/
├── README.md              # This file
├── config.py              # Configuration, imports, and constants
├── tools.py               # Tool function definitions
├── agents.py              # Agent definitions and configurations
├── sessions.py            # Session service setup and management
├── interactions.py        # Interaction functions and conversation logic
├── guardrails.py          # Guardrail callback functions
├── main.py                # Main entry point (refactored)
├── main_full.py           # Full script version with all code inline
├── main.ipynb             # Jupyter notebook version
└── requirements.txt       # Python dependencies
```

## File Descriptions

### config.py
- **Purpose**: Handles initial setup, library imports, API key configuration, and model constants.
- **Key Components**:
  - Google ADK imports
  - API key setup (Google Gemini)
  - Model constants (e.g., `MODEL_GEMINI_2_0_FLASH`)
  - Warning suppression and logging configuration

### tools.py
- **Purpose**: Defines all tool functions used by agents.
- **Key Components**:
  - `get_weather()`: Basic weather retrieval tool
  - `say_hello()`: Greeting tool with optional name parameter
  - `say_goodbye()`: Farewell tool
  - `get_weather_stateful()`: State-aware weather tool that respects user preferences

### agents.py
- **Purpose**: Contains all agent definitions and configurations.
- **Key Components**:
  - `weather_agent`: Basic weather agent
  - `greeting_agent`: Specialized greeting agent
  - `farewell_agent`: Specialized farewell agent
  - `weather_agent_team`: Root agent coordinating sub-agents
  - Various stateful and guardrail-enhanced agent versions

### sessions.py
- **Purpose**: Manages session services and state initialization.
- **Key Components**:
  - `InMemorySessionService` setup
  - Session creation functions
  - Stateful session initialization with user preferences

### interactions.py
- **Purpose**: Handles user-agent interactions and conversation execution.
- **Key Components**:
  - `call_agent_async()`: Core function for sending queries to agents
  - Various conversation functions (`run_conversation`, `run_team_conversation`, etc.)
  - State inspection utilities

### guardrails.py
- **Purpose**: Defines callback functions for input and tool guardrails.
- **Key Components**:
  - `block_keyword_guardrail()`: Blocks queries containing specific keywords
  - `block_paris_tool_guardrail()`: Blocks weather queries for specific cities

### main.py
- **Purpose**: Serves as the main entry point for the application.
- **Function**: Imports from all modules and provides a simple interface to run the system.

### main_full.py
- **Purpose**: Contains the full monolithic script with all code inline.
- **Function**: Self-contained version for easy execution without modular imports.

## System Initialization Flow

1. **Configuration Loading** (`config.py`):
   - Import required libraries
   - Set up API keys and environment variables
   - Define model constants
   - Configure logging and warnings

2. **Tool Definition** (`tools.py`):
   - Define tool functions with their logic
   - Tools are loaded into memory for agent use

3. **Session Setup** (`sessions.py`):
   - Initialize `InMemorySessionService`
   - Create sessions with optional initial state
   - Set up session identifiers (app_name, user_id, session_id)

4. **Agent Creation** (`agents.py`):
   - Define individual agents with their tools and instructions
   - Create sub-agents for specialized tasks
   - Build root agents that coordinate sub-agents
   - Apply guardrails and state management

5. **Runner Initialization**:
   - Create `Runner` instances linking agents to session services
   - Prepare for asynchronous execution

## Data Flow

### User Query Processing:
1. User query → `call_agent_async()` in `interactions.py`
2. Query formatted into ADK `Content` object
3. Runner executes agent logic asynchronously
4. Agent processes query through:
   - **Model Call**: LLM generates response (potentially intercepted by guardrails)
   - **Tool Execution**: If needed, tools are called (potentially blocked by guardrails)
   - **Sub-agent Delegation**: Root agent may delegate to specialized sub-agents
5. Final response returned to user

### State Management:
- Session state persists across interactions
- Tools can read/write state (e.g., user preferences, last actions)
- Guardrails can modify state (e.g., trigger flags)
- State is stored in `InMemorySessionService`

### Guardrail Flow:
- **Input Guardrail** (`before_model_callback`): Checks user input before LLM call
- **Tool Guardrail** (`before_tool_callback`): Validates tool arguments before execution
- If guardrail triggers, returns predefined response instead of proceeding

## Overall System Function

The system operates as a conversational AI assistant with the following capabilities:

1. **Weather Information**: Provides weather reports for cities using mock data
2. **State Awareness**: Remembers user preferences (e.g., temperature units) across sessions
3. **Multi-Agent Coordination**: Delegates tasks to specialized sub-agents
4. **Guardrails**: Prevents certain inputs or tool usages for safety/compliance
5. **Session Persistence**: Maintains conversation context and state

### Key Features:
- Asynchronous execution using `asyncio`
- Modular agent architecture with sub-agent delegation
- Stateful conversations with persistent user preferences
- Input and tool-level guardrails for content control
- Extensible tool system for adding new capabilities

## Usage

### Running the System:
```bash
cd agent_team
python main.py
```

### Running Specific Conversations:
Modify `main.py` to call desired conversation functions:
- `run_conversation()`: Basic weather agent
- `run_team_conversation()`: Multi-agent team
- `run_stateful_conversation()`: State-aware interactions
- `run_guardrail_test_conversation()`: Test input guardrails
- `run_tool_guardrail_test()`: Test tool guardrails

### Configuration:
- Set your Google API key in `config.py`
- Adjust model constants for different LLM providers
- Modify tool logic in `tools.py` for real weather data integration
- Customize guardrail rules in `guardrails.py`

## Dependencies

See `requirements.txt` for Python package requirements. Key dependencies:
- `google-adk`: Agent Development Kit
- `google-genai`: Google Generative AI library

## Testing

The refactored code maintains full compatibility with the original monolithic version. All conversation scenarios and edge cases should produce identical results. For testing:
1. Compare outputs between `main.py` and `main_full.py`
2. Verify state persistence across sessions
3. Test guardrail blocking behavior
4. Confirm sub-agent delegation works correctly

## Future Enhancements

- Integrate real weather APIs
- Add more specialized sub-agents
- Implement persistent storage (database instead of in-memory)
- Expand guardrail capabilities
- Add user authentication and multi-user support
