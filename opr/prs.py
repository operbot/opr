# This file is placed in the Public Domain.


"parse"


from .dft import Default
from .obj import register


def __dir__():
    return (
            "Parsed",
            "parse"
           )


class Parsed(Default):

    def __init__(self):
        Default.__init__(self)
        self.args = []
        self.gets = Default()
        self.sets = Default()
        self.toskip = Default()
        self.txt = ""

    def default(self, key, default=""):
        register(self, key, default)

    def parse(self, txt):
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


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    if "v" in prs.opts:
        prs.verbose = True
    return prs
