"""main"""
import os
import shutil
from functools import partial
from typing import Iterator
from typing import Dict
from typing import List
from typing import Callable

from typing import TypedDict

from open_data_parser.downloader import fetch_csv, read_csv, read_shapefile
from open_data_parser.transformer import transform
from open_data_parser.transformer import skip_header
from open_data_parser.transformer import concat_str
from open_data_parser.transformer import overwrite
from open_data_parser.transformer import set_latlon_order, filter_rows, shapeRecord2dict
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.writer import write_json
from open_data_parser.formatter import format_to_point, format_to_polygon


OUTPUT_BASE_PATH = "./data"


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
    # # 小規模保育園
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
            partial(query_coordinate_from_address, keys=["address", "name"]),
        ],
        formatter=format_to_point,
        writer=partial(
            write_json,
            path=f"{OUTPUT_BASE_PATH}/kosodate-map/",
            filename="syokibohoikuichiran.json",
        ),
    ),
    # 私立保育園
    Target(
        reader=partial(
            fetch_csv,
            url="https://www.city.funabashi.lg.jp/opendata/002/p059793_d/fil/sirituhoikusyoitiran.csv",
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
            partial(query_coordinate_from_address, keys=["address", "name"]),
        ],
        formatter=format_to_point,
        writer=partial(
            write_json, path="data/kosodate-map/", filename="sirituhoikusyoitiran.json"
        ),
    ),
    # 公立保育園
    Target(
        reader=partial(
            fetch_csv,
            url="https://www.city.funabashi.lg.jp/opendata/002/p059791_d/fil/korituhoikusyoitiran.csv",
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
            partial(query_coordinate_from_address, keys=["address", "name"]),
        ],
        formatter=format_to_point,
        writer=partial(
            write_json, path="data/kosodate-map/", filename="korituhoikusyoitiran.json"
        ),
    ),
    # 認定こども園
    Target(
        reader=partial(
            fetch_csv,
            url="https://www.city.funabashi.lg.jp/opendata/002/p059798_d/fil/ninteikodomoenitiran.csv",
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
            partial(query_coordinate_from_address, keys=["address", "name"]),
        ],
        formatter=format_to_point,
        writer=partial(
            write_json, path="data/kosodate-map/", filename="ninteikodomoenitiran.json"
        ),
    ),
    # 公民館
    Target(
        reader=partial(
            read_csv,
            path="./input/kosodate-map/kouminkan.csv",
            schema=[
                "id",
                "area",
                "name",
                "name_hurigana",
                "phone_number",
                "FAX_number",
                "zip_code",
                "address",
            ],
        ),
        transformers=[
            skip_header,
            partial(concat_str, key="address", value="船橋市"),
            partial(concat_str, key="name", value="公民館", from_left=False),
            partial(query_coordinate_from_address, keys=["address", "name"]),
        ],
        formatter=format_to_point,
        writer=partial(
            write_json, path="data/kosodate-map/", filename="kouminkan.json"
        ),
    ),
    # 医療機関
    Target(
        reader=partial(
            read_csv,
            path="./input/iryokikan/iryokikan.csv",
            schema=[
                "address",
                "name",
            ],
        ),
        transformers=[
            skip_header,
            partial(concat_str, key="address", value="船橋市"),
            partial(query_coordinate_from_address, keys=["address", "name"]),
            partial(overwrite, key="phone_number", value=""),  # 元データに電話番号が無いので上書き
        ],
        formatter=format_to_point,
        writer=partial(write_json, path="data/iryokikan/", filename="iryokikan.json"),
    ),
    Target(
        reader=partial(
            read_shapefile,
            path="./input/kosodate-map/polygon-gakku/A27-10_12-g_SchoolDistrict.shp",
        ),
        transformers=[
            partial(
                shapeRecord2dict,
                schema={
                    "name": ["A27_006", "A27_007"],
                    "inst_subject": ["A27_006"],
                    "address": ["A27_008"]
                }
                # shapefileの属性情報から
                # A27_006: 小学校の設置主体(ex:船橋市立)
                # A27_007: 小学校の名称
                # from https://nlftp.mlit.go.jp/ksj/gml/datalist/KsjTmplt-A27-v2_1.html
            ),
            partial(
                filter_rows, 
                filter_key="inst_subject", 
                filter_value="船橋市立"
            ),
            partial(set_latlon_order, coordinates_key="coordinates"),
        ],
        formatter=format_to_polygon,
        writer=partial(write_json, path="data/kosodate-map/", filename="gakku.json"),
    )
]


def main():
    """main"""

    # shutil.rmtree(OUTPUT_BASE_PATH)
    for target in TARGETS:
        
        raw_data = target["reader"]()

        transformed = transform(target["transformers"], raw_data)

        formatted = target["formatter"](transformed)

        target["writer"](data=list(formatted))


if __name__ == "__main__":
    main()
