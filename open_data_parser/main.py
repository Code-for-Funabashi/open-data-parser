"""main"""
from downloader import Downloader
from utils import get_geocode, combine_dicts
from transformer import transform

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
        "output_schema": [
            "name",
            "lat",
            "lon",
        ],
    }
]


def main():

    for row in TARGET:
        data = Downloader(row["url"], row["input_schema"])
        print(list(data.fetch()))
        # geo_coding(data)
        addends = get_geocode(data)
        
        output_records = list(map(combine_dicts, (data,addends)))

        # output schemaにデータ構造を揃える
        transformed_records = transform(records=output_records, output_schema=row["output_schema"])

        # csv filenameをjson filenameに利用する
        filename = os.path.basename(row["url"]).split(".csv")[0]
        with open(filename, "w+") as fp:
            json.dump(transformed_records, fp)


if __name__ == "__main__":
    main()
