import json
import os

CONFIG_FILE = "config.json"

def salvar_config(config):

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def carregar_config():

    if not os.path.exists(CONFIG_FILE):
        return None

    with open(CONFIG_FILE) as f:
        return json.load(f)

def config_existe():
    return os.path.exists(CONFIG_FILE)