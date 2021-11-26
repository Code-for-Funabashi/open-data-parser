""" test for downloader.py """

import unittest
from unittest import mock
from unittest.case import expectedFailure

import open_data_parser.downloader as target

# @mock.patch("request.urlopen")
# class TestFetchShapefile(unittest.TestCase):
#     def test_fetch_shapefile(self, client):
#         """Test query_coordinate_from_address() queries on a combined address """

#         data = [{"key1": "hoge", "key2": "fuga"}]

#         result = target.fetch_shapefile(data, ["key1", "key2"])
#         result.__next__()

#         client.return_value.geocode.assert_called_once_with("hoge fuga")
# unzip_shapefile


class TestUnzipShapefile(unittest.TestCase):
    def test_unzip_shapefile(self):
        import shapefile

        actual = target.unzip_shapefile(
            url="https://nlftp.mlit.go.jp/ksj/gml/data/A27/A27-10/A27-10_12_GML.zip",
            shp_fname="A27-10_12-g_SchoolDistrict.shp",
            dbf_fname="A27-10_12-g_SchoolDistrict.dbf",
        )
        self.assertIsInstance(actual, shapefile.ShapeRecords)


class TestCombineKeys(unittest.TestCase):
    def test_combine_keys(self):
        data = {
            "A27_005": "12100",
            "A27_006": "千葉市立",
            "A27_007": "こてはし台小学校",
            "A27_008": "千葉市花見川区こてはし台2-28-1",
        }
        new_schema = {
            "name": ["A27_006", "A27_007"],
            "institution_type": ["A27_006"],
            "address": ["A27_008"],
        }
        expected = {
            "name": "千葉市立 こてはし台小学校",
            "institution_type": "千葉市立",
            "address": "千葉市花見川区こてはし台2-28-1",
        }

        actual = target.combine_keys(data, new_schema)
        self.assertEqual(expected, actual)
