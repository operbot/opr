# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,C0411,R0903,R0904


"rss"


import unittest


from oper.rss import Fetcher


class TestRss(unittest.TestCase):

    def test_fetcher(self):
        fetcher = Fetcher()
        self.assertEqual(type(fetcher), Fetcher)
