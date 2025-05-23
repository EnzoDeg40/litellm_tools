import os
import litellm
from dotenv import load_dotenv
from rich import print
from rich.pretty import pretty_repr
import json

load_dotenv(override=True)

print("🤖 Using model:", os.environ["MODEL_NAME"])

names = []

tools = [
    {
        "type": "function",
        "function": {
            "name": "ajouter_nom",
            "description": "Ajoute un ou plusieurs prénoms à la liste",
            "parameters": {
                "type": "object",
                "properties": {
                    "prenoms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Les prénoms à ajouter"
                    }
                },
                "required": ["prenoms"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "supprimer_nom",
            "description": "Supprime un ou plusieurs prénoms de la liste",
            "parameters": {
                "type": "object",
                "properties": {
                    "prenoms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Les prénoms à supprimer"
                    }
                },
                "required": ["prenoms"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "liste_noms",
            "description": "Affiche les prénoms enregistrés",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

def add_name(prenoms: list):
    added = []
    for prenom in prenoms:
        names.append(prenom)
        added.append(prenom)
    return {"message": f"{', '.join(added)} ajouté(s)."}

def remove_name(prenoms: list):
    removed = []
    not_found = []
    for prenom in prenoms:
        if prenom in names:
            names.remove(prenom)
            removed.append(prenom)
        else:
            not_found.append(prenom)
    msg = ""
    if removed:
        msg += f"{', '.join(removed)} supprimé(s). "
    if not_found:
        msg += f"{', '.join(not_found)} n'était pas dans la liste."
    return {"message": msg.strip()}

def list_names():
    return {"liste": names if names else "Aucun prénom pour l'instant."}

def chat_loop():
    print("💬 Tape un message (ex: 'Ajoute Alice', 'Supprime Paul', 'Montre les noms')")
    while True:
        user_input = input("👤 Toi: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # Ajoute le contexte de la liste actuelle dans le message système
        system_message = {
            "role": "system",
            "content": f"Voici la liste actuelle des prénoms : {names if names else 'Aucun prénom'}"
        }

        # Appel du modèle
        response = litellm.completion(
            model=os.environ["MODEL_NAME"],
            messages=[system_message, {"role": "user", "content": user_input}],
            tools=tools,
            tool_choice="auto"
        )

        message = response['choices'][0]['message']
        
        tool_call = message.get('tool_calls')
        if tool_call:
            for call in tool_call:
                function_name = call['function']['name']
                arguments = json.loads(call['function']['arguments'])
                
                # Appel de la fonction correspondante
                if function_name == "ajouter_nom":
                    result = add_name(**arguments)
                elif function_name == "supprimer_nom":
                    result = remove_name(**arguments)
                elif function_name == "liste_noms":
                    result = list_names()
                
                print(pretty_repr(result))
        else:
            print("🤖", message['content'])

if __name__ == "__main__":
    chat_loop()
