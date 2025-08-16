import datetime
import os
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}


# Set up the model using LiteLLM with OpenRouter
# model = LiteLlm(model="gemini/gemini-2.5-flash")

# LITELLM_PROXY_URL = "http://localhost:4000"

# import litellm
# litellm._turn_on_debug()
# litellm.use_litellm_proxy = True
# litellm.litellm_proxy_api_base = os.getenv("LITELLM_PROXY_API_BASE", "http://localhost:4000")
# litellm.litellm_proxy_api_key = os.getenv("LITELLM_PROXY_API_KEY")



# Set up the LiteLLM model wrapper.
# The `model` parameter here is the name you configured in your LiteLLM proxy's config.yaml.
# The `base_url` is the crucial part that points the ADK to the proxy.
#model = LiteLlm(model="gemini/gemini-2.5-flash") # , base_url=LITELLM_PROXY_URL)
#model = LiteLlm(model="groq/llama-3.3-70b-versatile")
#model = LiteLlm(model="groq-llama3-8b-8192")
model = LiteLlm(model="huggingface/sambanova/meta-llama/Llama-3.3-70B-Instruct")

root_agent = Agent(
    name="weather_time_agent",
    #model="gemini-2.5-flash",
    model=model,
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)
