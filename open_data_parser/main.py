"""main"""
from functools import partial
from typing import Iterable
from typing import Dict
from typing import List
from typing import Callable

from typing import TypedDict

from open_data_parser.downloader import fetch_csv
from open_data_parser.transformer import add_city_name
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.writer import write_json
from open_data_parser.formatter.points import format_to_point


class Target(TypedDict):
    reader: Callable[..., Iterable[Dict[str, str]]]
    transformers: List[Callable[..., Iterable[Dict[str, str]]]]
    formatter: Callable[..., Iterable[Dict[str, str]]]
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
            # XXX: skip_header
            add_city_name,
            query_coordinate_from_address,
        ],
        formatter=format_to_point,
        writer=partial(
            write_json, path="data/kosodate-map/", filename="syokibohoikuichiran.json"
        ),
    )
]


def transform(
    transformers: List[Callable[[Iterable[Dict]], Iterable[Dict]]], data: Iterable[Dict]
) -> Iterable[Dict]:

    for transformer in transformers:
        data = transformer(data)

    return data


def main():
    for target in TARGETS:
        raw_data = target["reader"]()

        transformed = transform(target["transformers"], raw_data)

        target["writer"](data=list(transformed))


if __name__ == "__main__":
    main()
