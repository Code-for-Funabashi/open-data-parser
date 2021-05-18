""" test for transformer.py """

import unittest

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
