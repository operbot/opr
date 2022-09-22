# This file is placed in the Public Domain.


"runtime"


import time


starttime = time.time()


from .cfg import Config


Cfg = Config()


from .evt import Event


def docmd(clt, txt):
    cmd = Event()
    cmd.channel = ""
    cmd.orig = repr(clt)
    cmd.txt = txt
    clt.handle(cmd)
    cmd.wait()
    return cmd
