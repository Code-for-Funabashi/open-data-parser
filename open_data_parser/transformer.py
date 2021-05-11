"""transformer"""

from typing import Dict
from typing import Iterable
import os

import googlemaps

assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."


def query_coordinate_from_address(data: Iterable[Dict]) -> Iterable[Dict]:
    """Query the coordinate from the address."""
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)

    for record in data:
        # TODO:
        #  '山手1-3-17' / '本中山2-23-16'に大して、geocodeの返り値が[]になっていた。
        # 一方、”船橋市”を先頭に付けることで返り値がNULLで無くなった。
        lat, lng = gmaps.geocode(record["address"])[0]["geometry"]["location"]
        record.update({"lat": lat, "lng": lng})
        yield record
