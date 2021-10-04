""" test for downloader.py """

import unittest
from unittest import mock

import open_data_parser.downloader as target

@mock.patch("request.urlopen")
class TestFetchShapefile(unittest.TestCase):
    def test_fetch_shapefile(self, client):
        """Test query_coordinate_from_address() queries on a combined address """

        data = [{"key1": "hoge", "key2": "fuga"}]

        result = target.fetch_shapefile(data, ["key1", "key2"])
        result.__next__()

        client.return_value.geocode.assert_called_once_with("hoge fuga")
