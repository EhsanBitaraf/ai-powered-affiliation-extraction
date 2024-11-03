import json
from src.config import DATA_FILE

def load_dataset_mie():
    with open(DATA_FILE, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    return data