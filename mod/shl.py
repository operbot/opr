# This file is placed in the Public Domain.
# pylint: disable=C0116,C0413,W0212,C0301,W0613


"shell"


import atexit
import readline
import rlcompleter
import sys
import time


from opr.msg import Event
from opr.hdl import Command, Handler
from opr.obj import Wd, printable
from opr.run import Cfg


def __dir__():
    return (
            "Console",
            "shl"
           )


class Console(Handler):

    @staticmethod
    def announce(txt):
        pass

    @staticmethod
    def handle(event):
        Command.handle(event)
        event.wait()

    def poll(self):
        event = Event()
        event.txt = input("> ")
        event.orig = repr(self)
        return event

    @staticmethod
    def raw(txt):
        print(txt)
        sys.stdout.flush()


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        rlcompleter.Completer.__init__(self)
        self.matches = []
        self.options = options

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [
                                s for s in self.options
                                if s and s.startswith(text)
                               ]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None


def setcompleter(optionlist):
    completer = Completer(optionlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))


def shl(event):
    if Cfg.debug:
        return
    setcompleter(Command.cmd)
    date = time.ctime(time.time()).replace("  ", " ")
    print("%s started at %s %s" % (Cfg.name.upper(), date, printable(Cfg, "console,debug,verbose,wait", plain=True)))
    cli = Console()
    cli.start()
