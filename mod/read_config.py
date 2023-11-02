import os
import json


def readJson(file):
    with open(file, 'r') as config_:
        return json.load(config_)


def load():
    config_dir = os.path.abspath("./config")
    config_file_list = ["config.json", "config.cfg", "config.ini", "config.yml"]
    config_file = full_path = ""

    for root, dirs, files in os.walk(config_dir):
        for filename in files:
            if filename in config_file_list:
                config_file = filename
                full_path = os.path.join(config_dir, config_file)

    match config_file:
        case "":
            return None
        case "config.json":
            return readJson(full_path)
