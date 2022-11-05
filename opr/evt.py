# This file is placed in the Public Domain.
# pylint: disable=R,C,W,C0302


"event"


__version__ = "1"


## imports


import threading


from .hdl import Bus
from .obj import Default


## defines


def __dir__():
    return (
            'Event',
            'Parsed',
            'parse',
           )


__all__ = __dir__()


## classes


class Parsed(Default):

    def __init__(self):
        Default.__init__(self)
        self.args = []
        self.gets = Default()
        self.isparsed = False
        self.sets = Default()
        self.toskip = Default()
        self.txt = ""

    def default(self, key, default=""):
        register(self, key, default)

    def parse(self, txt=None):
        self.isparsed = True
        self.otxt = txt or self.txt
        spl = self.otxt.split()
        args = []
        _nr = -1
        for word in spl:
            if word.startswith("-"):
                try:
                    self.index = int(word[1:])
                except ValueError:
                    self.opts = self.opts + word[1:2]
                continue
            try:
                key, value = word.split("==")
                if value.endswith("-"):
                    value = value[:-1]
                    register(self.toskip, value, "")
                register(self.gets, key, value)
                continue
            except ValueError:
                pass
            try:
                key, value = word.split("=")
                register(self.sets, key, value)
                continue
            except ValueError:
                pass
            _nr += 1
            if _nr == 0:
                self.cmd = word
                continue
            args.append(word)
        if args:
            self.args = args
            self.rest = " ".join(args)
            self.txt = self.cmd + " " + self.rest
        else:
            self.txt = self.cmd


class Event(Parsed):

    def __init__(self):
        Parsed.__init__(self)
        self.__ready__ = threading.Event()
        self.control = "!"
        self.result = []
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def ready(self):
        self.__ready__.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self.__ready__.wait()


## utility


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    if "c" in prs.opts:
        prs.console = True
    if "v" in prs.opts:
        prs.verbose = True
    return prs
