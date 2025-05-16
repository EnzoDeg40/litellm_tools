import os
import json
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
    # not all models support multi-tooling
    model="azure/gpt-4o",
    messages=[{
        "role": "user",
        "content": "Combien font 5 + 7 et combien font 3 - 2 et combien font 10 - 3 ?"
    }],
    tools=tools,
    tool_choice="auto",
)

print("[bold yellow]Réponse brute :[/bold yellow]")
print(pretty_repr(response))

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

print("\n[bold green]Résultats des appels de fonctions :[/bold green]")
for tool_call in response.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    if name == "add_numbers":
        result = add_numbers(**args)
    elif name == "subtract_numbers":
        result = subtract_numbers(**args)
    else:
        result = f"[red]Fonction inconnue : {name}[/red]"

    print(f"🛠️ Appel de [bold]{name}({args})[/bold] → Résultat : [bold cyan]{result}[/bold cyan]")
