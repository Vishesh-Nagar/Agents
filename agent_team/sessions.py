# Session management and runners for agents.

from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()

APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

async def setup_session():
    global session
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

# Runner will be created after agents are imported

session_service_stateful = InMemorySessionService()
SESSION_ID_STATEFUL = "session_state_demo_001"
USER_ID_STATEFUL = "user_state_demo"

initial_state = {
    "user_preference_temperature_unit": "Celsius"
}

async def setup_stateful_session():
    global session_stateful
    session_stateful = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL,
        state=initial_state
    )
