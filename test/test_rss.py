# This file is placed in the Public Domain.


"rss"


import unittest


from mod.rss import Fetcher


class TestRss(unittest.TestCase):

    def test_fetcher(self):
        fetcher = Fetcher()
        self.assertEqual(type(fetcher), Fetcher)
