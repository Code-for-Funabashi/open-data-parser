"""writer"""
import os
import json


def write_json(path: str, filename: str, data):
    """Write data to json file."""
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{filename}", "w") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
