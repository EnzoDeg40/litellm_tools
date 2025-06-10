import os
import litellm
from dotenv import load_dotenv
from rich import print
from rich.pretty import pretty_repr

load_dotenv(override=True)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Gets the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g., Paris"}
                },
                "required": ["city"]
            }
        }
    }
]

response = litellm.completion(
    model="ollama/mistral",
    messages=[{"role": "user", "content": "Quelle est la météo à Lyon ?"}],
    tools=tools,
    tool_choice="auto",
)

print(response)

def get_weather(city):
    return f"La météo à {city} est ensoleillée avec une température de 25°C."

tool_call = response.choices[0].message.tool_calls[0]
args = eval(tool_call.function.arguments)

if tool_call.function.name == "get_weather":
    result = get_weather(**args)
else:
    raise ValueError(f"Unknown function: {tool_call.function.name}")
print(f"Résultat : {result}")
