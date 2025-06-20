import os
import litellm
from dotenv import load_dotenv
from rich import print
from rich.pretty import pretty_repr
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

load_dotenv(override=True)

tools = [
    {
        "type": "function",
        "function": {
            "name": "suggest_ideas",
            "description": "Add suggestions based on the conversation between the user and the assistant",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "array",
                        "items": {"type": "string"},
                    }
                },
                "required": ["context"]
            }
        }
    }
]

# Prompt système
system_message = {
    "role": "system",
    "content": (
        "Tu es un assistant. À partir du dernier message de l’utilisateur, propose exactement 3 suggestions pertinentes. "
        "Elles peuvent concerner des lieux précis, des dates spécifiques ou le voyage. "
        "Utilise l'outil 'suggest_ideas' pour ajouter des suggestions basées sur le contexte de la conversation. "
        "Les suggestions doivent être courtes, de quelques mots."
        "La date du jour est le " f"{datetime.datetime.now().strftime('(%A) %d-%m-%Y')}"
    )
}

conversation_history = [
    {"role": "assistant", "content": "Bonjour, comment puis-je t'aider aujourd'hui ?"},
    {"role": "user", "content": "J’ai envie de partir cet été proche de la mer"},
]

response = litellm.completion(
    model="ollama/gemma3:12b",
    messages=[system_message] + conversation_history,
    tools=tools,
    tool_choice="auto",
)

print("\n[bold cyan]Réponse brute du modèle :[/bold cyan]")
print(pretty_repr(response))

def suggest_ideas(context):
    print("\n[bold green]Suggestions basées sur ton contexte :[/bold green]")
    for i, idea in enumerate(context, 1):
        print(f"{i}. {idea}")

# Traitement de la réponse du modèle
tool_call = response.choices[0].message.tool_calls[0]
args = eval(tool_call.function.arguments)

if tool_call.function.name == "suggest_ideas":
    suggest_ideas(**args)
else:
    raise ValueError(f"Outil inconnu : {tool_call.function.name}")
