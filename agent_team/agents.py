# Agent definitions and runners.

import logging
from .config import MODEL
from google.adk.agents import Agent
from .tools import get_weather, say_hello, say_goodbye, translate_english_to_spanish

weather_agent = Agent(
    name="weather_agent",
    model=MODEL,
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "Only respond to queries about weather in specific cities. "
                "If the user specifies a city, use the 'get_weather' tool to retrieve the information. "
                "If no city is specified, politely ask the user to provide a city name. "
                "If the tool returns an error (e.g., city not found), inform the user politely that the weather for that city could not be retrieved and suggest trying another city. "
                "If the tool is successful, present the weather report clearly and concisely, including temperature, conditions, and any relevant details. "
                "Do not engage in unrelated conversations.",
    tools=[get_weather],
)

poem_agent = Agent(
    name="poem_agent",
    model=MODEL,
    description="Recites poems upon user request.",
    instruction="You are a poetic assistant. "
                "Only respond to requests for poems, including haikus, sonnets, or any poetic form. "
                "If the user requests a poem, provide one that is relevant to any themes, topics, or emotions mentioned. "
                "If no specific theme is given, create an original poem on a positive or inspirational topic. "
                "Ensure the response is solely the poem, without additional commentary unless necessary. "
                "If the request is not for a poem, do not respond.",
    tools=[],
)

translation_agent = Agent(
    name="translation_agent",
    model=MODEL,
    description="Translates English sentences to Spanish.",
    instruction="You are a translation assistant. "
                "Only handle requests to translate English text to Spanish. "
                "If the user provides an English sentence or phrase, use the 'translate_english_to_spanish' tool to attempt the translation. "
                "If the tool indicates that the translation is incomplete (e.g., some words not translated), use your knowledge to complete the translation accurately. "
                "Provide only the Spanish translation as the response, without any additional commentary. "
                "If the input is not in English or not a translation request, inform the user politely that you can only translate English to Spanish.",
    tools=[translate_english_to_spanish],
)

agent_team = Agent(
    name="agent_team",
    model=MODEL,
    description="The main coordinator agent. Handles greetings and farewell prompts and delegates requests to specialists.",
    instruction="You are the main Agent coordinating a team. "
                "Your primary responsibility is to handle greetings and farewells using the 'say_hello' and 'say_goodbye' tools. "
                "You have three specialized sub-agents: weather_agent, poem_agent, and translation_agent. "
                "Analyze the user's query carefully. "
                "If the query is a greeting (e.g., hello, hi), use 'say_hello'. "
                "If the query is a farewell (e.g., goodbye, bye), use 'say_goodbye'. "
                "If the query is about weather in a city, delegate to the weather_agent by passing the query. "
                "If the query requests a poem, delegate to the poem_agent. "
                "If the query is a translation from English to Spanish, delegate to the translation_agent. "
                "For any other query, respond politely that you can assist with greetings, weather, poems, or translations, and ask how you can help. "
                "Do not handle the delegated tasks yourself; always delegate to the appropriate sub-agent.",
    tools=[say_hello, say_goodbye],
    sub_agents=[weather_agent, poem_agent, translation_agent],
)
root_agent = agent_team

# Log when agents are called
logging.info("weather_agent initialized")
logging.info("poem_agent initialized")
logging.info("translation_agent initialized")
logging.info("agent_team (root_agent) initialized")
