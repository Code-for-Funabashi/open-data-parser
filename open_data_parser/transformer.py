"""transformer"""

from typing import Callable
from typing import Dict
from typing import List
from typing import Iterator
import os

import googlemaps

from open_data_parser.logger import logger


def transform(
    transformers: List[Callable[[Iterator[Dict]], Iterator[Dict]]], data: Iterator[Dict]
) -> Iterator[Dict]:
    """Call transformers in order."""

    for transformer in transformers:
        data = transformer(data)

    return data


def skip_header(data: Iterator[Dict]) -> Iterator[Dict]:
    """Skip the header record."""

    next(data)
    return data


def concat_str(
    data: Iterator[Dict], key: str, value: str, from_left: bool = True
) -> Iterator[Dict]:
    """Concat a string to the string with the given key."""

    for record in data:
        record[key] = value + record[key] if from_left else record[key] + value
        yield record


def query_coordinate_from_address(data: Iterator[Dict], keys: List[str]) -> Iterator[Dict]:
    """Query the coordinate from the address.
       GOOGLE_API_KEY is required because it uses googlemap's geocoding API
       see: https://developers.google.com/maps/documentation/geocoding/overview
    """

    assert os.environ.get("GOOGLE_API_KEY"), "Set your GOOGLE_API_KEY."
    googleapikey = os.environ["GOOGLE_API_KEY"]
    gmaps = googlemaps.Client(key=googleapikey)


    for record in data:
        target = " ".join([record[key] for key in keys])

        try:
            location = gmaps.geocode(target)[0]["geometry"]["location"]
        except Exception as err:
            logger.error("geocode error occured: err=%s, address=%s", err, target)
            raise err
        record.update({"lat": location["lat"], "lng": location["lng"]})
        yield record


def overwrite(
    data: Iterator[Dict], key: str, value: str
) -> Iterator[Dict]:
    """Overwrite the target key"""

    for record in data:
        record[key] = value
        yield record
