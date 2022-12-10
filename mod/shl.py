# This file is placed in the Public Domain.
# pylint: disable=C0116,C0413,W0212


"shell"


import time


from opr import Cfg, Command, Console, printable, setcompleter


def shl(event):
    setcompleter(Command.cmd)
    date = time.ctime(time.time()).replace("  ", " ")
    print("OPR started at %s %s" % (date, printable(Cfg, "console,debug,verbose,wait", plain=True)))
    cli = Console()
    cli.start()
