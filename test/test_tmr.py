# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0104


"timer"


import unittest


from opr.threads import Timer


def test():
    pass


class TestTimer(unittest.TestCase):

    def testcontructor(self):
        timer = Timer(60, test)
        self.assertEqual(type(timer), Timer)
