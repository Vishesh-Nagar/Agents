# Agent definitions and runners.

from config import MODEL_GEMINI_2_0_FLASH
from google.adk.agents import Agent
from guardrails import block_keyword_guardrail, block_paris_tool_guardrail
from sessions import APP_NAME, session_service_stateful
from tools import get_weather, say_hello, say_goodbye, get_weather_stateful

weather_agent = Agent(
    name="weather_agent_v1",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather],
)

greeting_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="greeting_agent",
    instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
    description="Handles simple greetings and hellos using the 'say_hello' tool.",
    tools=[say_hello],
)

farewell_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="farewell_agent",
    instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
    description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
    tools=[say_goodbye],
)

weather_agent_team = Agent(
    name="weather_agent_v2",
    model=MODEL_GEMINI_2_0_FLASH,
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                "You have specialized sub-agents: "
                "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                "If it's a weather request, handle it yourself using 'get_weather'. "
                "For anything else, respond appropriately or state you cannot handle it.",
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent]
)

root_agent_stateful = Agent(
    name="weather_agent_v4_stateful",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Main agent: Provides weather (state-aware unit), delegates greetings/farewells, saves report to state.",
    instruction="You are the main Weather Agent. Your job is to provide weather using 'get_weather_stateful'. "
                "The tool will format the temperature based on user preference stored in state. "
                "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                "Handle only weather requests, greetings, and farewells.",
    tools=[get_weather_stateful],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_weather_report"
)

from google.adk.runners import Runner

runner_root_stateful = Runner(
    agent=root_agent_stateful,
    app_name=APP_NAME,
    session_service=session_service_stateful
)

root_agent_model_guardrail = Agent(
    name="weather_agent_v5_model_guardrail",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
    instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                "Handle only weather requests, greetings, and farewells.",
    tools=[get_weather_stateful],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_weather_report",
    before_model_callback=block_keyword_guardrail
)

runner_root_model_guardrail = Runner(
    agent=root_agent_model_guardrail,
    app_name=APP_NAME,
    session_service=session_service_stateful
)

root_agent_tool_guardrail = Agent(
    name="weather_agent_v6_tool_guardrail",
    model=MODEL_GEMINI_2_0_FLASH,
    description="Main agent: Handles weather, delegates, includes input AND tool guardrails.",
    instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                "Delegate greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                "Handle only weather, greetings, and farewells.",
    tools=[get_weather_stateful],
    sub_agents=[greeting_agent, farewell_agent],
    output_key="last_weather_report",
    before_model_callback=block_keyword_guardrail,
    before_tool_callback=block_paris_tool_guardrail
)

runner_root_tool_guardrail = Runner(
    agent=root_agent_tool_guardrail,
    app_name=APP_NAME,
    session_service=session_service_stateful
)
