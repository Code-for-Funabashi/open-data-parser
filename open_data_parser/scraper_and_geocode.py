from bs4 import BeautifulSoup
import pandas as pd
from urllib import request
import ssl
import os
import googlemaps

def get_facility_categories():

    url=f"https://www.city.funabashi.lg.jp/funakkonavi/map/0/index.html"
    context = ssl._create_unverified_context()
    response = request.urlopen(url, context=context)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.select("select#category-map")
    results = res[0].find_all()
    id2CategoryType = {idx:t.text for idx, t in enumerate(results[1:])}
    return id2CategoryType


def get_tables(id2CategoryType):
    """
    全カテゴリの施設の名前、住所などを取得する関数
    """
    all_facilities = {}
    for i in range(13):
        url=f"https://www.city.funabashi.lg.jp/funakkonavi/map/{i}/index.html"
        context = ssl._create_unverified_context()
        response = request.urlopen(url, context=context)
        html = response.read()
        category = id2CategoryType[i]
        print(category)
        try:
            facilities = pd.read_html(html, )
        except ValueError as e:
            print(f"ValueError: No tables found for https://www.city.funabashi.lg.jp/funakkonavi/map/{i}/index.html")
            facilities = []
        all_facilities[category] = facilities
    return all_facilities
    

def main(id2CategoryType):
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)

    all_facilities = get_tables(id2CategoryType)
    for k in all_facilities.keys():
        print(k)
        print(len(all_facilities[k]))
        if len(all_facilities[k]) == 0:
            continue
        r = all_facilities[k][0]["住所"].map(lambda loc: gmaps.geocode(loc))
        all_facilities[k][0]["geocodes"] = r.map(lambda x: x[0]['geometry']["location"], na_action="ignore")

    
    # saving data.
    for k in all_facilities.keys():
        print("Saving as csv:", k)
        print(len(all_facilities[k]))
        if len(all_facilities[k]) == 0:
            continue
        all_facilities[k][0].to_csv(f"{k}.csv", index=False)
    return "Done!"

if __name__ == '__main__':
    id2CategoryType = get_facility_categories()
    print(main(id2CategoryType))