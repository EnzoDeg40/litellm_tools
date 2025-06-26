import os
import json
import litellm
from dotenv import load_dotenv
from rich import print
from rich.pretty import pretty_repr

load_dotenv(override=True)

MAX_TOOL_CALLS = 5

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
    },
    {
        "type": "function",
        "function": {
            "name": "done",
            "description": "when all tasks are completed, call this function to indicate completion.",
        }
    }
]

def add_numbers(a, b):
    return a + b

def subtract_numbers(a, b):
    return a - b

def done():
    print("[bold green]Toutes les tâches sont terminées ![/bold green]")

user_prompt = "Combien font 5 + 7 et combien font 3 - 2 et combien font 10 - 3 ?"

messages = [
    {"role": "system", "content": "Tu es un assistant qui doit répondre à la question en appelant les fonctions add_numbers et subtract_numbers. Pour chaque opération, appelle la fonction correspondante avec les bons arguments. Une fois toutes les opérations effectuées, appelle la fonction done. Voici l'historique des outils déjà appelés (nom et arguments, sans résultat) :"},
    {"role": "user", "content": user_prompt}
]

called_tools = []
results = []
done_called = False
nb_tool_calls = 0

while not done_called and nb_tool_calls < MAX_TOOL_CALLS:
    if called_tools:
        history = "\n".join([
            f"{tool['name']}({tool['arguments']})" for tool in called_tools
        ])
        messages.append({
            "role": "system",
            "content": f"Outils déjà appelés :\n{history}"
        })

    print("[bold magenta]Historique complet des messages :[/bold magenta]")
    for idx, msg in enumerate(messages, 1):
        print(f"[{idx}] {msg['role']}: {msg['content']}")

    response = litellm.completion(
        model="ollama/gemma3:12b",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    print("[bold yellow]Réponse brute :[/bold yellow]")
    print(pretty_repr(response))

    tool_calls = getattr(response.choices[0].message, "tool_calls", [])
    if not tool_calls:
        print("[red]Aucun appel d'outil détecté ![/red]")
        break

    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        called_tools.append({"name": name, "arguments": args})

        nb_tool_calls += 1

        if name == "add_numbers":
            result = add_numbers(**args)
            results.append((name, args, result))
            print(f"🛠️ Appel de [bold]{name}({args})[/bold] → Résultat : [bold cyan]{result}[/bold cyan]")
        elif name == "subtract_numbers":
            result = subtract_numbers(**args)
            results.append((name, args, result))
            print(f"🛠️ Appel de [bold]{name}({args})[/bold] → Résultat : [bold cyan]{result}[/bold cyan]")
        elif name == "done":
            done()
            done_called = True
        else:
            print(f"[red]Fonction inconnue : {name}[/red]")

if nb_tool_calls >= MAX_TOOL_CALLS and not done_called:
    print(f"[red]Limite de {MAX_TOOL_CALLS} appels d'outils atteinte, arrêt de la boucle pour éviter une boucle infinie.[/red]")

print("\n[bold green]Résumé des résultats :[/bold green]")
for name, args, result in results:
    print(f"{name}({args}) = [bold cyan]{result}[/bold cyan]")
