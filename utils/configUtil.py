import os
import json

def get_config(config_path):
    try:
        with open(config_path) as file:
            config = json.load(file)
            return config
    except Exception as e:
        print(f"Error while fetching secrets: {str(e)}")


config_path = "config/config.json"

try:
    config = get_config(config_path)
    print("config loaded")
except Exception as e:
    print(f"Error while fetching secrets: {str(e)}")