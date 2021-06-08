""" formatter for points """

from typing import Dict
from typing import Iterator


def format_to_point(records: Iterator[Dict]) -> Iterator[Dict]:

    for row in records:

        if "phone_number" not in row:
            # 電話番号が存在しないfeatureに対応
            row["phone_number"] = ""

        yield {
            "name": row["name"],
            "lat": row["lat"],
            "lng": row["lng"],
            "details": {
                "address": row["address"],
                "phone_number": row["phone_number"],
            },
        }
