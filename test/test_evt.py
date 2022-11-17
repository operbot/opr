# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,C0411,R0903,R0904


"event"


__version__ = "1"


## imports


import unittest


from opr.handler import Event


## classes


class TestEvent(unittest.TestCase):

    def testconstructor(self):
        evt = Event()
        self.assertEqual(type(evt), Event)
