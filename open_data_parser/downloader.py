"""Download Data"""
import csv
from json.encoder import py_encode_basestring
import shapefile
from urllib import request

from typing import Dict
from typing import List
from typing import Iterator


def fetch_csv(url: str, schema: List[str]) -> Iterator[Dict]:
    """
    urlからファイルをダウンロードし、定義されたスキーマのデータを返却する
    """
    with request.urlopen(url) as response:
        return csv.DictReader(response.read().decode("sjis").split("\r\n"), schema)


def read_csv(path: str, schema: List[str]) -> Iterator[Dict]:
    """
    localに配置させたcsv fileからデータを読み込み、定義されたスキーマのデータを返却する
    """
    return csv.DictReader(open(path, "r"), schema)

def read_shapefile(path: str) -> Iterator[shapefile.ShapeRecord]:
    """
    localに配置させたcsv fileからデータを読み込み、
    国土数値情報shapefileのスキーマのデータを返却する
    Output: Iterator[Dict]
        keys of Dict:
            name:
            (example) ['12100', '千葉市立', 'こてはし台小学校', '千葉市花見川区こてはし台2-28-1']

            coordinates:
            (example)
                ```
                [
                    [
                    (longitude, latitude),
                    ...
                    ]
                ]
                ```
    """
    shape = shapefile.Reader(path, encoding="sjis")
    features = shape.shapeRecords()
    return features
