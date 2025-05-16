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
            "name": "extract_flight_booking_info",
            "description": "Extracts flight booking details from user message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "adults": {"type": "integer"},
                    "segments": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "from": {"type": "string"},
                                "to": {"type": "string"},
                                "date": {"type": "string", "format": "date-time"},
                                "fromType": {"type": "string", "enum": ["0", "1"]},
                                "toType": {"type": "string", "enum": ["0", "1"]}
                            },
                            "required": ["from", "to", "date", "fromType", "toType"]
                        }
                    }
                },
                "required": ["adults", "segments"]
            }
        }
    }
]

response = litellm.completion(
    model="ollama/mistral",
    messages=[{"role": "user", "content": "Je veux réserver un vol de Paris à New York pour 2 adultes le 12 juin"}],
    tools=tools,
    tool_choice="auto",
)

print(response)

def extract_flight_booking_info(adults, segments):
    return {
        "adults": adults,
        "segments": segments
    }

tool_call = response.choices[0].message.tool_calls[0]
args = eval(tool_call.function.arguments)

if tool_call.function.name == "extract_flight_booking_info":
    result = extract_flight_booking_info(**args)
else:
    raise ValueError(f"Unknown function: {tool_call.function.name}")
print(f"Résultat : {result}")
