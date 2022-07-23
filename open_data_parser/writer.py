"""writer"""
import os
import json

import yaml


def write_json(path: str, filename: str, data):
    """Write data to json file."""
    os.makedirs(path, exist_ok=True)
    with open(f"{path}/{filename}", "w") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def create_json_from_yaml(input_filepath: str, output_path: str, output_filename):
    """create meta data for input data"""

    with open(input_filepath) as fp:
        obj = yaml.safe_load(fp)
    write_json(output_path, output_filename, obj)
