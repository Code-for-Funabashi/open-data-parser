"""transformer"""

from typing import Dict
from typing import Iterator
import os

from open_data_parser.logger import logger

import googlemaps

assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."


def skip_header(data: Iterator[Dict]) -> Iterator[Dict]:
    """Skip the header record."""

    next(data)
    return data


def concat_str(data: Iterator[Dict]) -> Iterator[Dict]:
    """Concat a string to the string with the given key."""

    for record in data:
        record["address"] = f"船橋市{record['address']}"
        yield record


def query_coordinate_from_address(data: Iterator[Dict]) -> Iterator[Dict]:
    """Query the coordinate from the address."""
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)

    for record in data:
        try:
            location = gmaps.geocode(record["address"])[0]["geometry"]["location"]
        except Exception as err:
            logger.error("geocode error occured: err=%s, address=%s", err, record['address'])
            raise err
        record.update({"lat": location["lat"], "lng": location["lng"]})
        yield record
