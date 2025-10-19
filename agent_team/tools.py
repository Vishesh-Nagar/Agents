# Tool functions for agent interactions.

from google.adk.tools.tool_context import ToolContext
from typing import Optional

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo").

    Returns:
        dict: A dictionary containing the weather information.
              Includes a 'status' key ('success' or 'error').
              If 'success', includes a 'report' key with weather details.
              If 'error', includes an 'error_message' key.
    """
    city_normalized = city.lower().replace(" ", "")
    mock_weather_db = {
        "newyork": {"status": "success", "report": "The weather in New York is sunny with a temperature of 25°C."},
        "london": {"status": "success", "report": "It's cloudy in London with a temperature of 15°C."},
        "tokyo": {"status": "success", "report": "Tokyo is experiencing light rain and a temperature of 18°C."},
    }
    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": f"Sorry, I don't have weather information for '{city}'."}

def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting = f"Hello, {name}!"
    else:
        greeting = "Hello there!"
    return greeting

def say_goodbye() -> str:
    """Provides a simple farewell message to conclude the conversation."""
    return "Goodbye! Have a great day."

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius")
    city_normalized = city.lower().replace(" ", "")
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }
    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_value = temp_c
            temp_unit = "°C"
        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        tool_context.state["last_city_checked_stateful"] = city
        return result
    else:
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        return {"status": "error", "error_message": error_msg}
