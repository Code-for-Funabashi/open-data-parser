from dataclasses import dataclass
import os

import pandas as pd
import googlemaps

assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float


def query_coordinate_from_address(address: str) -> Coordinate:
    """Query the coordinate from the address."""
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)

    # TODO:
    #  '山手1-3-17' / '本中山2-23-16'に大して、geocodeの返り値が[]になっていた。
    # 一方、”船橋市”を先頭に付けることで返り値がNULLで無くなった。
    return Coordinate(**gmaps.geocode(address)[0]["geometry"]["location"])
