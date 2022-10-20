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


class TestSkipRows(unittest.TestCase):
    def test_skip_rows(self):
        data = [
            {"key1": "hoge", "key2": "funa"},
            {"key1": "fuga", "key2": "bashi"},
        ]
        expected = [
            {"key1": "fuga", "key2": "bashi"},
        ]

        actual = target.skip_rows(data, "key1", "hoge")

        self.assertEqual(list(actual), expected)


class TestRenameKey(unittest.TestCase):
    def test_rename_key(self):
        data = [
            {"key1": "hoge", "key2": "funa"},
            {"key1": "fuga", "key2": "bashi"},
        ]
        expected = [
            {"key1": "hoge", "renamed_key": "funa"},
            {"key1": "fuga", "renamed_key": "bashi"},
        ]

        actual = target.rename_key(data, "key2", "renamed_key")

        self.assertEqual(list(actual), expected)


class TestToDict(unittest.TestCase):
    def test_to_dict(self):
        data = [
            {
                "name": "田喜野井旭こども園",
                "lat": 35.703267,
                "lng": 140.042440,
            },
            {
                "name": "うみのほいくえん",
                "lat": 35.695792,
                "lng": 139.983968,
            },
        ]
        expected = {
            "田喜野井旭こども園": {
                "name": "田喜野井旭こども園",
                "lat": 35.703267,
                "lng": 140.042440,
            },
            "うみのほいくえん": {
                "name": "うみのほいくえん",
                "lat": 35.695792,
                "lng": 139.983968,
            },
        }

        actual = target.to_dict(data, "name")

        self.assertEqual(actual, expected)


class TestMergeWithDict(unittest.TestCase):
    def test_merge_with_dict(self):
        data = [
            {
                "name": "田喜野井旭こども園",
                "key1": "hoge",
            },
            {
                "name": "うみのほいくえん",
                "key1": "fuga",
            },
        ]
        master_data = {
            "田喜野井旭こども園": {
                "name": "田喜野井旭こども園",
                "lat": 35.703267,
                "lng": 140.042440,
            },
            "うみのほいくえん": {
                "name": "うみのほいくえん",
                "lat": 35.695792,
                "lng": 139.983968,
            },
        }
        expected = [
            {
                "name": "田喜野井旭こども園",
                "key1": "hoge",
                "lat": 35.703267,
                "lng": 140.042440,
            },
            {
                "name": "うみのほいくえん",
                "key1": "fuga",
                "lat": 35.695792,
                "lng": 139.983968,
            },
        ]

        actual = target.merge_with_dict(data, master_data, "name")

        self.assertEqual(list(actual), expected)
