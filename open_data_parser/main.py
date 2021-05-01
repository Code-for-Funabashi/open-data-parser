"""main"""
from downloader import Downloader

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
        "output_schema": {},
    }
]


def main():

    for row in TARGET:
        data = Downloader(row["url"], row["input_schema"])
        print(list(data.fetch()))
        # geo_coader(data)


if __name__ == "__main__":
    main()
