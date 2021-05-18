"""writer"""
import json
import os
import shutil


def write_json(path: str, filename: str, data):
    """Write data to json file."""
    shutil.rmtree(path)
    os.makedirs(path)
    with open(f"{path}/{filename}", "w") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
