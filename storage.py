import json 
from config import HISTORY_FILE

def load_history():
    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(history):
    "saving the conversation history into json file"
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)