# This file is placed in the Public Domain.


"path tests"


import unittest


from opr.object import fntime


FN = "opr.handler.Event/45722f80dfec4867a1faf82bea059db0/2022-04-11/22:40:31.259218"


class TestPath(unittest.TestCase):

    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.259218)
