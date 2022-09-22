# This file is placed in the Public Domain.


"event"


import threading


from .bus import Bus
from .dft import Default
from .obj import update
from .prs import parse


def __dir__():
    return (
            "Event",
           )


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._result = []
        self.orig = repr(self)
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self):
        if self.txt:
            update(self, parse(self.txt))

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self._result.append(txt)

    def show(self):
        for txt in self._result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        return self._result
