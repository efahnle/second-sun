import json


def load_config(file_path="config.json"):
    """Load configuration from a JSON file."""
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Configuration file {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the configuration file {file_path}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while loading the configuration: {e}")
        return None
