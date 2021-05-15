import json
import os
from typing import List, Dict, T
import pandas as pd
import glob
from utils import csv2json


if __name__ == "__main__":
    print(os.path.dirname(os.path.realpath(__file__)))
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = f"{dirpath}/projects/kosodate-map/*.csv"
    path_list = glob.glob(filepath)
    for path in path_list:
        df = pd.read_csv(path)
        df = df.rename({'施設名':"name","住所": "address",'電話番号(代表)': "phone_number",}, axis=1)
        
        filename = os.path.basename(path)
        dicts = csv2json(df, cols_to_move=["address", "phone_number"])
        with open(f"{dirpath}/projects/kosodate-map/{filename.split('.')[0]}.json", "w+") as fp:
            json.dump(dicts, fp)
    