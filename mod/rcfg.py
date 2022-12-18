# This file is placed in the Public Domain


"runtime config"


from opr.obj import last, printable, keys, edit, write
from opr.run import Cfg


def __dir__():
    return (
            "rcfg",
           ) 


def rcfg(event):
    last(Cfg)
    if not event.sets:
        event.reply(printable(
                              Cfg,
                              keys(Cfg),
                             )
                   )
    else:
        edit(Cfg, event.sets)
        write(Cfg)
        event.done()
