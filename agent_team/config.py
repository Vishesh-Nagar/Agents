# Configuration and setup for the agent team project.

import logging
import warnings
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

load_dotenv()

MODEL = "gemini-2.0-flash"
