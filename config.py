import json

def load_config():
    with open("network_config.json", "r") as file:
        return json.load(file)
