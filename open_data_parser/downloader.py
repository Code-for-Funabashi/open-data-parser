"""Download Data"""
import csv
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
