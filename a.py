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
            "name": "add_numbers",
            "description": "Add two integers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtract_numbers",
            "description": "Subtract two integers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    }
]

response = litellm.completion(
    model="ollama/mistral",
    messages=[{"role": "user", "content": "Fais la soustraction de 10 et 3"}],
    tools=tools,
    tool_choice="auto",
)

print(response)

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

tool_call = response.choices[0].message.tool_calls[0]
args = eval(tool_call.function.arguments)

if tool_call.function.name == "add_numbers":
    result = add_numbers(**args)
elif tool_call.function.name == "subtract_numbers":
    result = subtract_numbers(**args)
else:
    raise ValueError(f"Unknown function: {tool_call.function.name}")
print(f"Résultat : {result}")
