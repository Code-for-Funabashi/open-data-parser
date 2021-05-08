"""Transform Data"""
import csv
from urllib import request

from typing import Dict
from typing import List, Set
from typing import Iterable

def transform(records: Iterable[Dict], output_schema: Set)->Iterable[Dict]:
    """
    Downloaderの返す Iterable[Dict]をoutput schemaに合わせて加工する。
    """
    transformed_records = []
    for r in records:
        transformed_r = {"detailed":{}}
        # FIXME:
        # output_schemaで第一階層でkeyとして持つ情報以外は全てdetailedに入れちゃう仕様で作っている。
        # 表示する必要のない不要なカラム等をどこで制御する？frontendでやるべきでしょうか？
        for col in output_schema:
            if r.get(col):
                transformed_r[col] = r.pop(col)
        transformed_r["detailed"].update(r)
        transformed_records.append(transformed_r)

    return transformed_records


