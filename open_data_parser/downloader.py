"""Download Data"""
import csv
from urllib import request

from typing import Dict
from typing import List
from typing import Iterable


class Downloader:
    """
    urlからファイルをダウンロードし、定義されたスキーマのデータを返却する
    """

    def __init__(self, url: str, schema: List[str]):
        self.url = url
        self.schema = schema

    def _download(self):
        response = request.urlopen(self.url)
        return response.read().decode("sjis").split("\r\n")

    def fetch(self) -> Iterable[Dict]:
        return csv.DictReader(self._download(), self.schema)
