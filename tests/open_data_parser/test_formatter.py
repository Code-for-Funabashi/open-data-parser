""" test for formatter.py """
import unittest
from unittest import mock

import open_data_parser.formatter as target


class TestformatToPoint(unittest.TestCase):
    def test_format_to_point(self):
        data = [
            {
                "name": "田喜野井旭こども園",
                "lat": 35.703267,
                "lng": 140.042440,
                "foo": "hoge",
                "bar": "funa",
            },
            {
                "name": "うみのほいくえん",
                "lat": 35.695792,
                "lng": 139.983968,
                "foo": "fuga",
                "bar": "bashi",
            },
        ]
        expected = [
            {
                "name": "田喜野井旭こども園",
                "lat": 35.703267,
                "lng": 140.042440,
                "details": {"foo": "hoge", "bar": "funa"},
            },
            {
                "name": "うみのほいくえん",
                "lat": 35.695792,
                "lng": 139.983968,
                "details": {"foo": "fuga", "bar": "bashi"},
            },
        ]

        actual = target.format_to_point(data, ["foo", "bar"])

        self.assertEqual(list(actual), expected)
