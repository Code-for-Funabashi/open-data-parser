""" formatter for points """

from typing import Dict
from typing import Iterator


def format_to_point(records: Iterator[Dict]) -> Iterator[Dict]:

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


def format_to_polygon(records: Iterator[Dict]) -> Iterator[Dict]:
    """
    'coordinates' key のみ下記のようにformat変更する
      From: List[(point_1), (point_2), ... ,(point_n)]
      To: List[List[(point_1), (point_2), ... ,(point_n)]]
    """
    for row in records:
        yield {
            "name": row["name"],
            "coordinates": [row["coordinates"]]
        }
