""" test for transformer.py """

import unittest
from unittest import mock

import open_data_parser.transformer as target


class TestSkipHeader(unittest.TestCase):
    """Test for skip_header()"""

    def test_skip_header(self):
        """Test skip_header() skips the first row."""

        class IntIterator:

            cnt = 0
            limit = 3

            def __iter__(self):
                return self

            def __next__(self):
                if self.cnt == self.limit:
                    raise StopIteration()

                self.cnt += 1
                return self.cnt

        actual = target.skip_header(IntIterator())
        self.assertEqual(list(actual), [2, 3])


class TestConcatStr(unittest.TestCase):
    def test_concat_str(self):
        """Test concat_str() adds string for the value of the target key."""

        data = [{"target": "hoge"}, {"target": "fuga"}]

        value = "piyo"

        expected = [{"target": "piyohoge"}, {"target": "piyofuga"}]

        actual = target.concat_str(data, key="target", value=value)
        self.assertEqual(list(actual), expected)


@mock.patch("googlemaps.Client")
class TestQueryCoordinateFromAddress(unittest.TestCase):
    def test_query_coordinate_from_address(self, client):
        """Test query_coordinate_from_address() queries on a combined address"""

        data = [{"key1": "hoge", "key2": "fuga"}]

        result = target.query_coordinate_from_address(data, ["key1", "key2"])
        result.__next__()

        client.return_value.geocode.assert_called_once_with("hoge fuga")


class TestOverwrite(unittest.TestCase):
    def test_overwrite(self):
        """Test overwrite() overwrites element."""

        data = [{"key1": "hoge"}, {"key1": "fuga"}]

        expected = [{"key1": "piyo"}, {"key1": "piyo"}]

        actual = target.overwrite(data, key="key1", value="piyo")
        self.assertEqual(list(actual), expected)

    def test_overwrite_creates_new_elemet(self):
        """Test overwrite() creates new element"""

        data = [{"key1": "hoge"}, {"key1": "fuga"}]

        expected = [{"key1": "hoge", "key2": "piyo"}, {"key1": "fuga", "key2": "piyo"}]

        actual = target.overwrite(data, key="key2", value="piyo")
        self.assertEqual(list(actual), expected)


class TestFilterRows(unittest.TestCase):
    def test_filter_rows(self):
        """Test filter_rows() filters elements."""

        data = [
            {"key1": "hoge", "key2": "funa"},
            {"key1": "fuga", "key2": "bashi"},
        ]

        expected = [{"key1": "hoge", "key2": "funa"}]

        actual = target.filter_rows(data, filter_key="key2", filter_value="funa")
        self.assertEqual(list(actual), expected)


class TestReverseLatLonOrder(unittest.TestCase):
    def test_reverse_latlon_order(self):
        data = [
            {
                "name": "船橋市立 海神小学校",
                "coordinates": [
                    [
                        [139.984168, 35.708842],
                        [139.982974, 35.708799],
                    ]
                ],
            }
        ]
        expected = [
            {
                "name": "船橋市立 海神小学校",
                "coordinates": [
                    [
                        [35.708842, 139.984168],
                        [35.708799, 139.982974],
                    ]
                ],
            }
        ]
        actual = target.reverse_latlon_order(data, coordinates_key="coordinates")
        self.assertEqual(list(actual), expected)


class TestTransformPointCrs(unittest.TestCase):


    def test_transform_point_crs(self):
        wgs84_epsg = 4326
        tokyo_epsg = 4301
        data = [{"lng": 138.385554841666, "lat": 34.9748902437125}]

        expected = [{"lng": 138.38246584906943, "lat": 34.978172333217344}]

        actual = target.transform_point_crs(data, "lat", "lng", tokyo_epsg, wgs84_epsg)
        self.assertEqual(list(actual), expected)
