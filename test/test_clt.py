# This file is placed in the Public Domain.
# pylint: disable=C0113,C0114,C0115,C0116


import unittest


from opr.clt import Client


class MyClient(Client):

    gotcha = False

    def raw(self, txt):
        MyClient.gotcha = True


class TestClient(unittest.TestCase):

    def setUp(self):
        MyClient.gotcha = False

    def test_clienteneedsraw(self):
        with self.assertRaises(NotImplementedError):
            clt = Client()
            clt.raw("bla")

    def test_clienthasraw(self):
        clt = MyClient()
        clt.raw("txt")
        self.assertTrue(clt.gotcha)
