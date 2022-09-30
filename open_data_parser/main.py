"""main"""
import shutil
from functools import partial
from typing import Iterator
from typing import Dict
from typing import List
from typing import Callable

from typing import TypedDict

from open_data_parser.downloader import read_csv
from open_data_parser.downloader import read_json
from open_data_parser.downloader import read_excel
from open_data_parser.downloader import fetch_shapefile
from open_data_parser.transformer import transform
from open_data_parser.transformer import to_dict
from open_data_parser.transformer import skip_header
from open_data_parser.transformer import merge_with_dict
from open_data_parser.transformer import reverse_latlon_order
from open_data_parser.transformer import filter_rows
from open_data_parser.transformer import skip_rows
from open_data_parser.transformer import rename_key
from open_data_parser.transformer import concat_str
from open_data_parser.transformer import query_coordinate_from_address
from open_data_parser.writer import write_json
from open_data_parser.formatter import format_to_point
from open_data_parser.formatter import format_to_polygon
from open_data_parser.writer import create_json_from_yaml


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
    # 保育園
    Target(
        reader=partial(
            read_excel,
            path="./input/kosodate-map/hoikuen.xlsx",
            sheet_name="入所可能性一覧",
            skiprows=9,
            usecols="E,H:M",
            schema=(
                "name",
                "acceptable_0yo",
                "acceptable_1yo",
                "acceptable_2yo",
                "acceptable_3yo",
                "acceptable_4yo",
                "acceptable_5yo",
            ),
        ),
        transformers=[
            # partial(concat_str, key="name", value="保育園", from_left=False),
            partial(
                merge_with_dict,
                master_data=to_dict(
                    read_json("./input/masterdata/hoikuen.json"), "name"
                ),
                key="name",
            ),
        ],
        formatter=partial(
            format_to_point,
            details_schema=[
                "address",
                "phone_number",
                "type",
                "capacity",
                "acceptable_age",
                "acceptable_0yo",
                "acceptable_1yo",
                "acceptable_2yo",
                "acceptable_3yo",
                "acceptable_4yo",
                "acceptable_5yo",
            ],
        ),
        writer=partial(write_json, path="data/kosodate-map/", filename="hoikuen.json"),
    ),
    # # 公民館
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
    # # 小学校区
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
]


def main():
    """main"""
    shutil.rmtree(OUTPUT_BASE_PATH)
    for target in TARGETS:

        raw_data = target["reader"]()

        transformed = transform(target["transformers"], raw_data)

        formatted = target["formatter"](transformed)

        target["writer"](data=list(formatted))

    # create metadata
    create_json_from_yaml("input/meta.yml", "data", "meta.json")


if __name__ == "__main__":
    main()
