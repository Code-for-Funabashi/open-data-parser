"""Download Data"""
import csv
import json
from urllib import request
import zipfile
import io
from typing import Dict
from typing import List
from typing import Iterator
from typing import Optional
import shapefile
from shapely.geometry import shape
from shapely.geometry import mapping
import pandas as pd



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


def read_json(path: str) -> Dict:
    """
    localに配置させたjson fileからデータを読み込みスキーマのデータを返却する
    """
    return json.load(open(path, "r"))


def unzip_shapefile(url: str, shp_fname: str, dbf_fname: str) -> shapefile.ShapeRecords:
    """
    urlからzipファイルをダウンロードし、shapeRecordsを返す
    """
    with request.urlopen(url) as response:
        content = response.read()
        with zipfile.ZipFile(io.BytesIO(content)) as f:
            shp = f.open(shp_fname)
            dbf = f.open(dbf_fname)
            reader = shapefile.Reader(shp=shp, dbf=dbf, encoding="sjis")
    return reader.shapeRecords()


def combine_keys(data: Dict, new_schema: Dict[str, List[str]]) -> Dict:
    """
    複数のkeysの要素を結合して、new_keyを作る
    Args:
        data: Dict
            example: {"A": "val_a", "B": "val_b"}
        new_schema: Dict
            example: {"AB": ["A", "B"]}
    Returns:
        Dict:
            example: {"AB": "val_a val_b"}
    """
    output = {}
    for new_key, old_keys in new_schema.items():
        output[new_key] = " ".join([data[key] for key in old_keys])
    return output


def fetch_shapefile(
    url: str, shp_fname: str, dbf_fname: str, reformed_schema: Dict = {}
) -> Iterator[Dict]:
    """
    urlからshapefileの含まれた、zipデータを読み込み、
    shapefileのスキーマを再編して辞書データを返却する
    """
    features = unzip_shapefile(url, shp_fname, dbf_fname)
    for feature in features:
        output = {}
        coords = shape(feature.shape.__geo_interface__)
        # add coords
        output.update(mapping(coords))
        # add formatted feature-info
        record = feature.record.as_dict()
        output.update(combine_keys(record, reformed_schema))
        yield output


def read_excel(
    path: str,
    sheet_name: str,
    schema: list[str],
    skiprows: int = 0,
    skipfooter: int = 0,
    usecols: Optional[str] = None,
) -> Iterator[Dict]:
    """
    localに配置させたExcelファイルからデータを読み込み、定義されたスキーマのデータを返却する
    """
    book = pd.ExcelFile(path)
    sheet = book.parse(
        sheet_name,
        skiprows=skiprows,
        skipfooter=skipfooter,
        usecols=usecols,
        names=schema,
        dtype="object",
    ).fillna(0)
    for _, row in sheet.iterrows():
        yield row.to_dict()
