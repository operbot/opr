# This file is placed in the Public Domain.
# pylint: disable=R0903,C0103,C0114,C0115,C0116,W0622


import time


from opr.obj import Wd, find, fntime, keys, printable
from opr.utl import elapsed


def fnd(event):
    if not event.args:
        res = ",".join(sorted([x.split(".")[-1].lower() for x in Wd.types()]))
        if res:
            event.reply(res)
        else:
            event.reply("no types yet.")
        return
    bot = event.bot()
    otype = event.args[0]
    nmr = 0
    for obj in find(otype, event.gets):
        txt = "%s %s %s" % (
                            str(nmr),
                            printable(obj, event.sets.keys or keys(obj), event.toskip),
                            elapsed(time.time()-fntime(obj.__fnm__))
                           )
        nmr += 1
        event.reply(txt)
    if not nmr:
        event.reply("no result")
