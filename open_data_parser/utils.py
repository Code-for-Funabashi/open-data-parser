import os
import json
from bs4 import BeautifulSoup
import pandas as pd
from typing import List
from typing import Dict
import googlemaps
from downloader import Downloader

assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."
googleapikey = os.environ["GOOGLE_API_KEY"]
gmaps = googlemaps.Client(key=googleapikey)


combine_dicts = lambda x, y: {**x, **y}

def csv2json(df:pd.DataFrame, cols_to_move:List) -> List[Dict]:
    # "name", "lat", "lng", "details"の4keyのjson形式データを生成する関数
    # detailsに入れ子格納したいカラム、存在するものだけ持ってくる。
    
    df["details"] = df.loc[:, df.columns.isin(cols_to_move)].to_dict("records")
    dicts = df[["name", "lat", "lng", "details"]].to_dict("records")
    return dicts



def get_geocode(data:Downloader) -> Dict:
    """
     args: 
       data: Downloader object
     return: 
       1 point location(latitude and longitude)
    """
    outputs = []
    facility_list = list(data.fetch())[1:]# headerを取り除く
    for facility in facility_list:
        try:
            out: Dict = gmaps.geocode(facility["address"])[0]
            outputs.append(out['geometry']["location"])
        except googlemaps.exceptions.HTTPError as HTTPError:
            print(f"HTTPError Occurred for {str(facility)}")
        except IndexError:
            print(f"検索結果が存在しませんでした。:{str(facility)}")
            # TODO:
            #  '山手1-3-17' / '本中山2-23-16'に大して、geocodeの返り値が[]になっていた。
            # 一方、”船橋市”を先頭に付けることで返り値がNULLで無くなった。
            # HACK:
            # とりあえず、再帰的にもう一度geocode処理実行
            out: Dict = gmaps.geocode("船橋市"+facility["address"])[0]
            outputs.append(out['geometry']["location"])

    return outputs
