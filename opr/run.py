# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0209,W0212,W1514,R1732

"runtime"


## import


import atexit
import os
import readline
import rlcompleter
import sys
import termios
import time


from .obj import Default, keys, update
from .hdl import Command, parse
from .thr import name


## define


Cfg = Default()


def __dir__():
    return (
            "banner",
            "daemon",
            'from_exception',
            "setcompleter",
            "wrap"
           )


__all__ = __dir__()


## class


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        super().__init__()
        self.matches = []
        self.options = options

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None


## utility


def banner(name):
    print(
          "%s started at %s" % (
                                name.upper(),
                                time.ctime(time.time()).replace("  ", " "),
                               )
         )


def boot(name):
    setcompleter(keys(Command.cmd))
    txt = ' '.join(sys.argv[1:])
    cfg = parse(txt)
    update(Cfg, cfg)
    banner(name)
    return cfg


def daemon(silent=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open("/dev/null", 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    if silent:
        sos = open("/dev/null", 'a+')
        ses = open("/dev/null", 'a+')
        os.dup2(sos.fileno(), sys.stdout.fileno())
        os.dup2(ses.fileno(), sys.stderr.fileno())


def from_exception(exc, txt="", sep=" "):
    result = []
    for frm in traceback.extract_tb(exc.__traceback__):
        fnm = os.sep.join(frm.filename.split(os.sep)[-2:])
        result.append(f"{fnm}:{frm.lineno}")
    nme = name(exc)
    res = sep.join(result)
    return f"{txt} {res} {nme}: {exc}"


def setcompleter(optionlist):
    completer = Completer(optionlist)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    readline.redisplay()
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)

