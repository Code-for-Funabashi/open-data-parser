"""transformer"""

from typing import Dict
from typing import List
from typing import Iterable
import os

import googlemaps

assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."


def add_city_name(data: Iterable[Dict]) -> Iterable[Dict]:

    for record in data:
        record["address"] = f"船橋市{record['address']}"
        yield record


def query_coordinate_from_address(data: Iterable[Dict]) -> Iterable[Dict]:
    """Query the coordinate from the address."""
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)

    for record in data:
        try:
            lat, lng = gmaps.geocode(record['address'])[0]["geometry"]["location"]
        except Exception as err:
            print(err, record["address"])
        record.update({"lat": lat, "lng": lng})
        yield record
