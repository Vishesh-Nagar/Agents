# Configuration and setup for the agent team project.

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import asyncio
import os
import logging
import warnings

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
