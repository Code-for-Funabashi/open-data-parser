import json
import os
from typing import List, Dict, T
import pandas as pd
import glob



def csv2json(df:pd.DataFrame, cols_to_move:List) -> List[T]:
    # "name", "lat", "lng", "details"の4keyのjson形式データを生成する関数
    # detailsに入れ子格納したいカラム、存在するものだけ持ってくる。
    
    df["details"] = df.loc[:, df.columns.isin(cols_to_move)].to_dict("records")
    dicts = df[["name", "lat", "lng", "details"]].to_dict("records")
    return dicts

