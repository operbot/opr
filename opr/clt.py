# This file is placed in the Public Domain.


"client"


from .com import dispatch
from .hdl import Handler


def __dir__():
    return (
            "Client",
           )


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.ignore = []
        self.orig = repr(self)
        self.register("event", dispatch)

    def announce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        if channel not in self.ignore:
            self.raw(txt)
