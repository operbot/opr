# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"handler"


import unittest


from opr.handler import Handler


class TestHandler(unittest.TestCase):

    def testconstructor(self):
        hdl = Handler()
        self.assertEqual(type(hdl), Handler)
