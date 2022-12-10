#!/usr/bin/env python3
# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0411,C0413


"runtime"


import atexit
import importlib
import importlib.util
import os
import readline
import rlcompleter
import sys
import termios
import traceback


from opr.handler import Cfg, Client, Command, Event, parse, scan
from opr.thread import launch

class CLI(Client):

    def announce(self, txt):
        pass

    def raw(self, txt):
        print(txt)
        sys.stdout.flush()


class Console(CLI):

    def handle(self, event):
        Command.handle(event)
        event.wait()

    def poll(self):
        event = Event()
        event.txt = input("> ")
        event.orig = repr(self)
        return event


class Completer(rlcompleter.Completer):

    def __init__(self, options):
        super().__init__()
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


def boot(txt):
    parse(txt)
    if "c" in Cfg.opts:
        Cfg.console = True
    if "d" in Cfg.opts:
        Cfg.daemon = True
    if "v" in Cfg.opts:
        Cfg.verbose = True
    if "w" in Cfg.opts:
        Cfg.wait = True
    if "x" in Cfg.opts:
        Cfg.exec = True


def daemon():
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    os.umask(0)
    sis = open("/dev/null", 'r')
    os.dup2(sis.fileno(), sys.stdin.fileno())
    if not Cfg.verbose:
        sos = open("/dev/null", 'a+')
        ses = open("/dev/null", 'a+')
        os.dup2(sos.fileno(), sys.stdout.fileno())
        os.dup2(ses.fileno(), sys.stderr.fileno())


def importer(pname, mname, path=None, init=False):
    if not path:
        path = pname
    mod = None
    spec = importlib.util.spec_from_file_location(mname, path)
    if spec:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        scan(mod)
    if init and "init" in dir(mod):
        launch(mod.init)        
    return mod


def print_exc(ex):
    traceback.print_exception(type(ex), ex, ex.__traceback__)


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
