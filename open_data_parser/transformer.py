"""transformer"""

from typing import Any
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


def query_coordinate_from_address(
    data: Iterator[Dict], keys: List[str]
) -> Iterator[Dict]:
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


def overwrite(data: Iterator[Dict], key: str, value: str) -> Iterator[Dict]:
    """Overwrite the target key"""

    for record in data:
        record[key] = value
        yield record


def reverse_latlon_order(data: Iterator[Dict], coordinates_key: str) -> Iterator[Dict]:
    """reverse 'lonlat' order to 'latlon' one"""
    for record in data:
        coord_exteriors_and_holes = record[coordinates_key]
        record[coordinates_key] = [
            list(map(lambda coord: coord[::-1], coords))
            for coords in coord_exteriors_and_holes
        ]
        yield record


def filter_rows(
    data: Iterator[Dict], filter_key: str, filter_value: str
) -> Iterator[Dict]:
    """Skip the records which are not targeted."""

    for record in data:
        if record[filter_key] == filter_value:
            yield record


def skip_rows(data: Iterator[Dict], filter_key: str, value: Any) -> Iterator[Dict]:
    """Skip if the value of the target key is given value"""

    for record in data:
        if record[filter_key] == value:
            continue
        yield record


def rename_key(data: Iterator[Dict], from_: str, to: str) -> Iterator[Dict]:
    """Rename keys"""

    for record in data:
        record[to] = record[from_]
        del record[from_]

        yield record

def to_dict(data: Iterator[dict], key: str) -> dict[str, Any]:
    """
    Iterator[dict] を、keyのdictに変換する
    """

    res = {}

    for row in data:
        res[row[key]]= row

    return res

def merge_with_dict(data: list[dict], master_data: dict, key: str) -> Iterator[dict]:
    """
    与えられたkeyを元に、master_dataとdataをmergeする。
    """

    for row in data:
        if row[key] not in master_data:
            logger.warning("%s がマスターデータに存在しません。マスターデータの情報が最新か確認してください", row[key])
            continue
        row.update(master_data[row[key]])
        yield row
