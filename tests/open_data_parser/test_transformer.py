""" template """

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
