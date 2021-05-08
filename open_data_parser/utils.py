import json
from bs4 import BeautifulSoup
import pandas as pd
from typing import List
from typing import Dict
from typing import T
from typing import Union
from urllib import request
import ssl
import os
import googlemaps


assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."
googleapikey = os.environ["GOOGLE_API_KEY"]
gmaps = googlemaps.Client(key=googleapikey)


combine_dicts = lambda x, y: {**x, **y}

def csv2json(df:pd.DataFrame, cols_to_move:List) -> List[T]:
    # "name", "lat", "lng", "details"の4keyのjson形式データを生成する関数
    # detailsに入れ子格納したいカラム、存在するものだけ持ってくる。
    
    df["details"] = df.loc[:, df.columns.isin(cols_to_move)].to_dict("records")
    dicts = df[["name", "lat", "lng", "details"]].to_dict("records")
    return dicts



def get_geocode(address:Union[List, str]) -> Dict:
    """
     args: 
       address: google APIで叩くための住所情報
     return: 
       1 point location(latitude and longitude)
    """
    if isinstance(address, list):
        outputs = []
        for addr_ in address:
            out: Dict = gmaps.geocode(addr_)
            outputs.append(out['geometry']["location"])
        return outputs
    else:
        output_dict: Dict = gmaps.geocode(address)
        return output_dict['geometry']["location"]