# Agent definitions and runners.

from config import MODEL
from google.adk.agents import Agent
from tools import get_weather, say_hello, say_goodbye

weather_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather],
)

poem_agent = Agent(
    name="poem_agent",
    model=MODEL,
    description="Recites poems upon user request.",
    instruction="You are a poetic assistant. "
                "When the user requests a poem, respond with a well-known poem or create a new one. "
                "Make sure the poem is relevant to any themes or topics mentioned by the user.",
    tools=[],
)

agent_team = Agent(
    name="root_agent",
    model=MODEL,
    description="The main coordinator agent. Handles greetings and farewell prompts and delegates weather/time requests to specialists.",
    instruction="You are the main Agent coordinating a team. Your primary responsibility is to greet the user with the given tools. "
                "Use the 'say_hello' tool to greet the user and the 'say_goodbye' tool to bid farewell."
                "You have two specialized sub-agents: "
                "1. 'weather_agent': Handles weather request for specific cities. Delegate to it for these. "
                "2. 'poem_agent': Handles queries for reciting a poem. Delegate to it for these. "
                "Analyze the user's query. If it's a greeting or a farewell, respond using the say_hello and say_goodbye functions. "
                "If it's a weather request, delegate it to the weather_agent along with the city. "
                "If it's a poem request, delegate it to the poem_agent. "
                "For anything else, respond appropriately or state you cannot handle it.",
    tools=[say_hello, say_goodbye],
    sub_agents=[weather_agent, poem_agent],
)
