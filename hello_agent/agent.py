from google.adk.agents.llm_agent import Agent

def get_current_time(city: str) -> dict[str, str]:
    return {
        'city': city,
        'current_time': '2024-06-01 12:00:00'
    }

def get_weather(city: str) -> dict[str, str]:
    return {
        'city': city,
        'weather': 'Sunny, 25°C'
    }

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Tell the current time and weather in a specified city',
    instruction='You are a helpful assistant that provides the current time and weather for a given city. Use `get_current_time` to get the current time and `get_weather` to get the weather information.',
    tools=[get_current_time, get_weather]
)
