"""main"""
from downloader import Downloader
from utils import get_geocode, combine_dicts
from transformer import transform
import os
import json
from pathlib import Path

TARGET = [
    {
        "url": "https://www.city.funabashi.lg.jp/opendata/002/p059795_d/fil/syokibohoikuichiran.csv",
        "input_schema": [
            "name",
            "address",
            "phone_number",
            "capacity",
            "established_at",
        ],
        # TODO:
        # TO act-taさん > output_schemaの記法どうしましょう？5/8に相談した時のschemaを失念している気がします。mm
        # 取り急ぎ、下記3つ以外の情報を全てdetailedに格納する方針で動いています。
        "output_schema": [
            "name",
            "lat",
            "lon",
        ],
        # TODO:
        # この仕様もちょっと悩ましい...
        "output_path":"projects/kosodate-map/小規模保育"
    }
]


def main():
    dir_path = Path(__file__).parent
    for row in TARGET:
        data = Downloader(row["url"], row["input_schema"])
        
        # ジオコーディング
        geocodes = get_geocode(data)

        # geocode と、施設情報のdictionaryを結合する
        output_records = list(map(combine_dicts, list(data.fetch()),geocodes))

        # output schemaにデータ構造を揃える
        transformed_records = transform(records=output_records, output_schema=row["output_schema"])

        # 出力
        filename = os.path.basename(row["output_path"])
        data_dir = os.path.dirname(row["output_path"])
        
        with open(dir_path / data_dir / f"{filename}.json", "w+") as fp:
            json.dump(transformed_records, fp)


if __name__ == "__main__":
    main()
