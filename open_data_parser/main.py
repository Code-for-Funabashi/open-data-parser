"""main"""
import os
import json
from pathlib import Path
from typing import Iterable
from typing import Dict
from typing import List
from typing import Callable

from open_data_parser.downloader import Downloader
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.formatter.points import format_to_point

TARGETS = [
    {
        "url": "https://www.city.funabashi.lg.jp/opendata/002/p059795_d/fil/syokibohoikuichiran.csv",
        "input_schema": [
            "name",
            "address",
            "phone_number",
            "capacity",
            "established_at",
        ],
        "transformer": [query_coordinate_from_address],
        "formatter": format_to_point,
        "output_path": "projects/kosodate-map/syokibohoikuichiran",
    }
]


def transform(transformers: List[Callable], data: Iterable[Dict]) -> Iterable[Dict]:

    for transformer in transformers:
        data = transformer(data)

    return data


def main():
    dir_path = Path(__file__).parent
    for target in TARGETS:
        raw_data = Downloader(target["url"], target["input_schema"]).fetch()

        transformed = transform(target["transformer"], raw_data)

        # 出力
        filename = os.path.basename(target["output_path"])
        data_dir = os.path.dirname(target["output_path"])

        with open(dir_path / data_dir / f"{filename}.json", "w+") as fp:
            json.dump(transformed, fp)


if __name__ == "__main__":
    main()
