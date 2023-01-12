# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"event"


import unittest


from opr.message import Event


class TestEvent(unittest.TestCase):

    def testconstructor(self):
        evt = Event()
        self.assertEqual(type(evt), Event)
