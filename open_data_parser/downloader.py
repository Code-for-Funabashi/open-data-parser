"""Download Data"""
import csv
from json.encoder import py_encode_basestring
import shapefile
from urllib import request
import zipfile
import io
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


def fetch_shapefile(
    url: str, shp_fname: str, dbf_fname: str, reformed_schema: Dict = {}
) -> Iterator[Dict]:
    """
    urlからshapefileの含まれた、zipデータを読み込み、
    shapefileのスキーマを再編して辞書データを返却する

    ## shapefileのスキーマの再編に関して
    例：国土数値情報の場合、地物情報が下記のように格納されているとする。
        sample_data = {
            'A27_005': '12100',
            'A27_006': '千葉市立',
            'A27_007': 'こてはし台小学校',
            'A27_008': '千葉市花見川区こてはし台2-28-1'
        }
    こちらを、reformed_schema引数を用いて、下記のように
    old_keysをconcatして、new_keyを作れるような処理を追加している、
    reformed_schema={
        "new_key": [key for key in old_keys]
    }
    例：
    reformed_schema = {
        "name":['A27_006', 'A27_007'],
        "institution_type":['A27_006'],
        "address":['A27_008'],
    }
    すると、sample_dataは、下記のように読み込まれる
    reformated_sample_data = {
        'name': '千葉市立 こてはし台小学校',
        'institution_type': '千葉市立',
        'address': '千葉市花見川区こてはし台2-28-1'
    }
    """
    with request.urlopen(url) as response:
        content = response.read()
        with zipfile.ZipFile(io.BytesIO(content)) as f:
            shp = f.open(shp_fname)
            dbf = f.open(dbf_fname)
            reader = shapefile.Reader(shp=shp, dbf=dbf, encoding="sjis")
    features = reader.shapeRecords()
    # shapefile.shapeRecords to List[Dict]
    for feat in features:
        record: Dict = feat.record.as_dict()
        record.update({"coordinates": feat.shape.points})
        record.update({"shape_parts": feat.shape.parts})
        # 既存string valueを持つkeysのconcat処理をfetch時に組み込んでみました。
        # 必要ない場合は、指定しなければreformed_schemaに空dictが渡され、この処理はskipされるようにしました。
        for new_key, original_keys in reformed_schema.items():
            record[new_key] = " ".join([record[key] for key in original_keys])
        # delete original keys
        for key in original_keys:
            record.pop(key)
        yield record
