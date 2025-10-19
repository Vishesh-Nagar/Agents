# Functions for interacting with agents asynchronously.

from agent_team.agents import weather_agent_team
from config import APP_NAME, USER_ID, SESSION_ID
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from sessions import session_service, runner, USER_ID, SESSION_ID, runner_root_stateful, session_service_stateful, USER_ID_STATEFUL, SESSION_ID_STATEFUL, runner_root_model_guardrail, runner_root_tool_guardrail

async def call_agent_async(query: str, runner, user_id, session_id):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce a final response."
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break
    return final_response_text

async def run_conversation():
    await call_agent_async("What is the weather like in London?", runner=runner, user_id=USER_ID, session_id=SESSION_ID)
    await call_agent_async("How about Paris?", runner=runner, user_id=USER_ID, session_id=SESSION_ID)
    await call_agent_async("Tell me the weather in New York", runner=runner, user_id=USER_ID, session_id=SESSION_ID)

async def run_team_conversation():
    session_service_team = InMemorySessionService()
    APP_NAME_TEAM = "weather_tutorial_agent_team"
    USER_ID_TEAM = "user_1_agent_team"
    SESSION_ID_TEAM = "session_001_agent_team"
    session_team = await session_service_team.create_session(
        app_name=APP_NAME_TEAM, user_id=USER_ID_TEAM, session_id=SESSION_ID_TEAM
    )
    actual_root_agent = weather_agent_team if 'weather_agent_team' in globals() else None
    if actual_root_agent:
        runner_agent_team = Runner(
            agent=actual_root_agent,
            app_name=APP_NAME_TEAM,
            session_service=session_service_team
        )
        await call_agent_async(query="Hello there!", runner=runner_agent_team, user_id=USER_ID_TEAM, session_id=SESSION_ID_TEAM)
        await call_agent_async(query="What is the weather in New York?", runner=runner_agent_team, user_id=USER_ID_TEAM, session_id=SESSION_ID_TEAM)
        await call_agent_async(query="Thanks, bye!", runner=runner_agent_team, user_id=USER_ID_TEAM, session_id=SESSION_ID_TEAM)

async def run_stateful_conversation():
    await call_agent_async(query="What's the weather in London?", runner=runner_root_stateful, user_id=USER_ID_STATEFUL, session_id=SESSION_ID_STATEFUL)
    stored_session = session_service_stateful.sessions[APP_NAME][USER_ID_STATEFUL][SESSION_ID_STATEFUL]
    stored_session.state["user_preference_temperature_unit"] = "Fahrenheit"
    await call_agent_async(query="Tell me the weather in New York.", runner=runner_root_stateful, user_id=USER_ID_STATEFUL, session_id=SESSION_ID_STATEFUL)
    await call_agent_async(query="Hi!", runner=runner_root_stateful, user_id=USER_ID_STATEFUL, session_id=SESSION_ID_STATEFUL)

async def run_guardrail_test_conversation():
    await call_agent_async("What is the weather in London?", runner_root_model_guardrail, USER_ID_STATEFUL, SESSION_ID_STATEFUL)
    await call_agent_async("BLOCK the request for weather in Tokyo", runner_root_model_guardrail, USER_ID_STATEFUL, SESSION_ID_STATEFUL)
    await call_agent_async("Hello again", runner_root_model_guardrail, USER_ID_STATEFUL, SESSION_ID_STATEFUL)

async def run_tool_guardrail_test():
    await call_agent_async("What's the weather in New York?", runner_root_tool_guardrail, USER_ID_STATEFUL, SESSION_ID_STATEFUL)
    await call_agent_async("How about Paris?", runner_root_tool_guardrail, USER_ID_STATEFUL, SESSION_ID_STATEFUL)
    await call_agent_async("Tell me the weather in London.", runner_root_tool_guardrail, USER_ID_STATEFUL, SESSION_ID_STATEFUL)
