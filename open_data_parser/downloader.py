"""Download Data"""
import csv
from urllib import request

from typing import Dict
from typing import List
from typing import Iterable


def fetch_csv(url: str, schema: List[str]) -> Iterable[Dict]:
    """
    urlからファイルをダウンロードし、定義されたスキーマのデータを返却する
    """
    with request.urlopen(url) as response:
        return csv.DictReader(response.read().decode("sjis").split("\r\n"), schema)
