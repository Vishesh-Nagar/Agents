# Tool functions for agent interactions.

import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

def get_weather(city: str) -> dict:
    """Retrieve current weather for a specified city using WeatherAPI.com."""
    
    api_key = os.getenv("WEATHERAPI_KEY")
    if not api_key:
        return {"status": "error", "error_message": "WEATHERAPI_KEY not set in .env file."}

    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get("current", {})
        condition = current.get("condition", {}).get("text")
        temp_c = current.get("temp_c")

        if condition and temp_c is not None:
            report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_c}°C."
            return {"status": "success", "report": report}
        else:
            return {"status": "error", "error_message": "Unexpected API response structure."}

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"Unexpected error: {e}"}
    
def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}! How can help you today"
    else:
        greeting = "Hello there! How can I help you?"
    return greeting

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    return "Goodbye! Have a great day."
