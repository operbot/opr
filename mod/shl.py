# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0411,C0413


"shell"


import sys
import termios
import threading
import time


from opr import Cfg, Client, Command, Event, launch, printable


class Shell(Client):

    def dispatch(self, event):
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


def wrap(func):
    fds = sys.stdin.fileno()
    gotterm = True
    try:
        old = termios.tcgetattr(fds)
    except termios.error:
        gotterm = False
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        threading.interrupt_main()
        print("")
    finally:
        if gotterm:
            termios.tcsetattr(fds, termios.TCSADRAIN, old)



def init():
    date = time.ctime(time.time()).replace("  ", " ")
    print("OPR started at %s %s" % (date, printable(Cfg, "console,debug,verbose,wait", plain=True)))
    shl = Shell()
    wrap(shl.start)
