# Load the data
# Clean the data
# Load into pre-created database
#    might need class of dbutils

import json


def load_data(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)

    return data
