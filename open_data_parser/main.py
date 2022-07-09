"""main"""
import os
import shutil
from functools import partial
from typing import Iterator
from typing import Dict
from typing import List
from typing import Callable

from typing import TypedDict

from open_data_parser.downloader import fetch_csv
from open_data_parser.downloader import read_csv
from open_data_parser.downloader import fetch_shapefile
from open_data_parser.transformer import transform
from open_data_parser.transformer import skip_header
from open_data_parser.transformer import concat_str
from open_data_parser.transformer import overwrite
from open_data_parser.transformer import reverse_latlon_order
from open_data_parser.transformer import filter_rows
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.transformer import skip_rows
from open_data_parser.transformer import rename_key
from open_data_parser.transformer import transform_point_crs
from open_data_parser.transformer import WGS84_EPSG
from open_data_parser.transformer import TOKYO_EPSG
from open_data_parser.writer import write_json
from open_data_parser.formatter import format_to_point
from open_data_parser.formatter import format_to_polygon


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
    # Target(
    #     reader=partial(
    #         fetch_csv,
    #         url="https://www.city.funabashi.lg.jp/opendata/002/p059795_d/fil/syokibohoikuichiran.csv",
    #         schema=[
    #             "name",
    #             "address",
    #             "phone_number",
    #             "capacity",
    #             "established_at",
    #         ],
    #     ),
    #     transformers=[
    #         skip_header,
    #         partial(concat_str, key="address", value="船橋市"),
    #         partial(query_coordinate_from_address, keys=["address", "name"]),
    #     ],
    #     formatter=format_to_point,
    #     writer=partial(
    #         write_json,
    #         path=f"{OUTPUT_BASE_PATH}/kosodate-map/",
    #         filename="syokibohoikuichiran.json",
    #     ),
    # ),
    # # 私立保育園
    # Target(
    #     reader=partial(
    #         fetch_csv,
    #         url="https://www.city.funabashi.lg.jp/opendata/002/p059793_d/fil/sirituhoikusyoitiran.csv",
    #         schema=[
    #             "name",
    #             "address",
    #             "phone_number",
    #             "capacity",
    #             "established_at",
    #         ],
    #     ),
    #     transformers=[
    #         skip_header,
    #         partial(concat_str, key="address", value="船橋市"),
    #         partial(query_coordinate_from_address, keys=["address", "name"]),
    #     ],
    #     formatter=format_to_point,
    #     writer=partial(
    #         write_json, path="data/kosodate-map/", filename="sirituhoikusyoitiran.json"
    #     ),
    # ),
    # # 公立保育園
    # Target(
    #     reader=partial(
    #         fetch_csv,
    #         url="https://www.city.funabashi.lg.jp/opendata/002/p059791_d/fil/korituhoikusyoitiran.csv",
    #         schema=[
    #             "name",
    #             "address",
    #             "phone_number",
    #             "capacity",
    #             "established_at",
    #         ],
    #     ),
    #     transformers=[
    #         skip_header,
    #         partial(concat_str, key="address", value="船橋市"),
    #         partial(query_coordinate_from_address, keys=["address", "name"]),
    #     ],
    #     formatter=format_to_point,
    #     writer=partial(
    #         write_json, path="data/kosodate-map/", filename="korituhoikusyoitiran.json"
    #     ),
    # ),
    # 認定こども園
    # Target(
    #     reader=partial(
    #         fetch_csv,
    #         url="https://www.city.funabashi.lg.jp/opendata/002/p059798_d/fil/ninteikodomoenitiran.csv",
    #         schema=[
    #             "name",
    #             "address",
    #             "phone_number",
    #             "capacity",
    #             "established_at",
    #         ],
    #     ),
    #     transformers=[
    #         skip_header,
    #         partial(concat_str, key="address", value="船橋市"),
    #         partial(query_coordinate_from_address, keys=["address", "name"]),
    #     ],
    #     formatter=format_to_point,
    #     writer=partial(
    #         write_json, path="data/kosodate-map/", filename="ninteikodomoenitiran.json"
    #     ),
    # ),
    # 公民館
    # Target(
    #     reader=partial(
    #         read_csv,
    #         path="./input/kosodate-map/kouminkan.csv",
    #         schema=[
    #             "id",
    #             "area",
    #             "name",
    #             "name_hurigana",
    #             "phone_number",
    #             "FAX_number",
    #             "zip_code",
    #             "address",
    #         ],
    #     ),
    #     transformers=[
    #         skip_header,
    #         partial(concat_str, key="address", value="船橋市"),
    #         partial(concat_str, key="name", value="公民館", from_left=False),
    #         partial(query_coordinate_from_address, keys=["address", "name"]),
    #     ],
    #     formatter=format_to_point,
    #     writer=partial(
    #         write_json, path="data/kosodate-map/", filename="kouminkan.json"
    #     ),
    # ),
    # 医療機関
    # Target(
    #     reader=partial(
    #         read_csv,
    #         path="./input/iryokikan/iryokikan.csv",
    #         schema=[
    #             "address",
    #             "name",
    #         ],
    #     ),
    #     transformers=[
    #         skip_header,
    #         partial(concat_str, key="address", value="船橋市"),
    #         partial(query_coordinate_from_address, keys=["address", "name"]),
    #         partial(overwrite, key="phone_number", value=""),  # 元データに電話番号が無いので上書き
    #     ],
    #     formatter=format_to_point,
    #     writer=partial(write_json, path="data/iryokikan/", filename="iryokikan.json"),
    # ),
    # Target(
    #     reader=partial(
    #         fetch_shapefile,
    #         url="https://nlftp.mlit.go.jp/ksj/gml/data/A27/A27-10/A27-10_12_GML.zip",
    #         shp_fname="A27-10_12-g_SchoolDistrict.shp",
    #         dbf_fname="A27-10_12-g_SchoolDistrict.dbf",
    #         reformed_schema={
    #             "name": ["A27_006", "A27_007"],
    #             "institution_type": ["A27_006"],
    #             "address": ["A27_008"],
    #         },
    #     ),
    #     transformers=[
    #         partial(filter_rows, filter_key="institution_type", filter_value="船橋市立"),
    #         partial(reverse_latlon_order, coordinates_key="coordinates"),
    #     ],
    #     formatter=format_to_polygon,
    #     writer=partial(write_json, path="data/kosodate-map/", filename="gakku.json"),
    # ),
    # 保育園
    Target(
        reader=partial(
            read_csv,
            path="./input/kosodate-map/hoikuen.csv",
            schema=[
                "shichoson_code",
                "number",
                "prefecture",
                "cities",
                "name",
                "name_kana",
                "type",
                "address",
                "katagaki",
                "lat",
                "lng",
                "access",
                "parking",
                "phone_number",
                "naisen_phone_number",
                "fax_number",
                "corporate_number",
                "corporate_name",
                "approval_date",
                "capacity",
                "acceptable_age",
                "available_day_of_week",
                "start_time",
                "end_time",
                "available_date_and_time_special_notes",
                "temporary_childcare",
                "url",
                "remarks",
                "waiting_0yo",
                "waiting_1yo",
                "waiting_2yo",
                "waiting_3yo",
                "waiting_4yo",
                "waiting_5yo",
                "waiting_all_yo",
                "lng_bodik",
                "lat_bodik",
            ],
        ),
        transformers=[
            skip_header,
            partial(skip_rows, filter_key="lng_bodik", value=""),
            partial(rename_key, from_="lng_bodik", to="lng"),
            partial(rename_key, from_="lat_bodik", to="lat"),
        ],
        formatter=partial(
            format_to_point,
            details_schema=[
                "number",
                "address",
                "phone_number",
                "capacity",
                "waiting_0yo",
                "waiting_1yo",
                "waiting_2yo",
                "waiting_3yo",
                "waiting_4yo",
                "waiting_5yo",
            ],
        ),
        writer=partial(write_json, path="data/kosodate-map/", filename="hoikuen.json"),
    ),
    Target(
        reader=partial(
            fetch_shapefile,
            url="https://nlftp.mlit.go.jp/ksj/gml/data/A27/A27-10/A27-10_12_GML.zip",
            shp_fname="A27-10_12-g_SchoolDistrict.shp",
            dbf_fname="A27-10_12-g_SchoolDistrict.dbf",
            reformed_schema={
                "name": ["A27_006", "A27_007"],
                "institution_type": ["A27_006"],
                "address": ["A27_008"],
            },
        ),
        transformers=[
            partial(filter_rows, filter_key="institution_type", filter_value="船橋市立"),
            partial(reverse_latlon_order, coordinates_key="coordinates"),
        ],
        formatter=format_to_polygon,
        writer=partial(write_json, path="data/kosodate-map/", filename="gakku.json"),
    ),
]


def main():
    """main"""
    shutil.rmtree(OUTPUT_BASE_PATH)
    for target in TARGETS:

        raw_data = target["reader"]()

        transformed = transform(target["transformers"], raw_data)

        formatted = target["formatter"](transformed)

        target["writer"](data=list(formatted))


if __name__ == "__main__":
    main()
