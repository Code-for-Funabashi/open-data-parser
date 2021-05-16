"""main"""
from functools import partial
from typing import Iterator
from typing import Dict
from typing import List
from typing import Callable

from typing import TypedDict

from open_data_parser.downloader import fetch_csv
from open_data_parser.transformer import transform
from open_data_parser.transformer import skip_header
from open_data_parser.transformer import concat_str
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.writer import write_json
from open_data_parser.formatter.points import format_to_point


class Target(TypedDict):
    """パーサーのターゲット。
       データの読み込み、加工、整形、出力を行う関数を登録する。

    Attributes:
        reader: パースするデータを読み込むするCallable
        transformers: readerで取得したデータを加工するCallableを指定した配列
        formatter: データを出力形式に整形するCallable
        writer: データを出力するCallable
    """

    reader: Callable[..., Iterator[Dict[str, str]]]
    transformers: List[Callable[..., Iterator[Dict[str, str]]]]
    formatter: Callable[..., Iterator[Dict[str, str]]]
    writer: Callable


TARGETS = [
    Target(
        reader=partial(
            fetch_csv,
            url="https://www.city.funabashi.lg.jp/opendata/002/p059795_d/fil/syokibohoikuichiran.csv",
            schema=[
                "name",
                "address",
                "phone_number",
                "capacity",
                "established_at",
            ],
        ),
        transformers=[
            skip_header,
            partial(concat_str, key="address", value="船橋市"),
            partial(query_coordinate_from_address, key="address"),
        ],
        formatter=format_to_point,
        writer=partial(
            write_json, path="data/kosodate-map/", filename="syokibohoikuichiran.json"
        ),
    )
]


def main():
    """main"""
    for target in TARGETS:
        raw_data = target["reader"]()

        transformed = transform(target["transformers"], raw_data)

        target["writer"](data=list(transformed))


if __name__ == "__main__":
    main()
