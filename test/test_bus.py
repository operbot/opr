# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,C0411,R0903,R0904


"bus"


import unittest


from opr import Bus, Handler


class Client(Handler):

    gotcha = False

    def announce(self, txt):
        Client.gotcha = True


class TestBus(unittest.TestCase):

    def test_construct(self):
        bus = Bus()
        self.assertEqual(type(bus), Bus)

    def test_add(self):
        bus = Bus()
        clt = Client()
        bus.add(clt)
        self.assertTrue(clt in bus.objs)

    def test_announce(self):
        bus = Bus()
        clt = Client()
        bus.add(clt)
        bus.announce("test")
        self.assertTrue(Client.gotcha)

    def test_byorig(self):
        bus = Bus()
        clt = Client()
        self.assertEqual(bus.byorig(repr(clt)), clt)

    def test_say(self):
        bus = Bus()
        clt = Client()
        bus.add(clt)
        bus.say(repr(clt), "#test", "test")
        self.assertTrue(Client.gotcha)
