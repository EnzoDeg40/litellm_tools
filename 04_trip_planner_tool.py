import os
import litellm
from dotenv import load_dotenv
from rich import print
from rich.pretty import pretty_repr

load_dotenv(override=True)

print("🤖 Using model:", os.environ["MODEL_NAME"])

tools = [
    {
        "type": "function",
        "function": {
            "name": "plan_trip",
            "description": "Planifie un trajet entre deux villes avec une date de départ.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from": {"type": "string", "description": "Code de la ville de départ (ex: CDG)"},
                    "to": {"type": "string", "description": "Code de la ville d'arrivée (ex: JFK)"},
                    "departure": {
                        "type": "string",
                        "description": "Date de départ au format YYYY-MM-DD",
                        "format": "date-time" # use data if you can
                    }
                },
                "required": ["from", "to", "departure"]
            }
        }
    }
]

response = litellm.completion(
    model=os.environ["MODEL_NAME"],
    messages=[
        {"role": "system", "content": "Nous sommes le 10 mai 2024 aka 2024-05-10. Les dates annonces par l'utilisateur est relative à cette date."},
        {"role": "user", "content": "Je veux aller de CDG à JFK le 25 mai"}, 
    ],
    tools=tools,
    tool_choice="auto",
)

print(pretty_repr(response))

def plan_trip(from_, to, departure):
    if "T" in departure:
        print(f"⚠️ Warning: Departure date '{departure}' contains 'T', removing time part.")
        departure = departure.split("T")[0]

    return f"Trajet prévu de {from_} à {to} le {departure}."

tool_call = response.choices[0].message.tool_calls[0]
args = eval(tool_call.function.arguments)

# warn 'from' is a reserved keyword in Python
args["from_"] = args.pop("from")

if tool_call.function.name == "plan_trip":
    result = plan_trip(**args)
else:
    raise ValueError(f"Unknown function: {tool_call.function.name}")

print(f"✅ Result : {result}")
