""" formatter for points """

from typing import Dict
from typing import Iterable


def format_to_point(records: Iterable[Dict]) -> Iterable[Dict]:

    for row in records:

        yield {
            "name": row["name"],
            "lat": row["lat"],
            "lng": row["lng"],
            "details": {
                "address": row["address"],
                "phone_number": row["phone_number"],
            },
        }
