# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E1101


"runtime information"


import threading
import time


from opr import Bus, Object, elapsed, name, update


def __dir__():
    return (
            'flt',
            'thr',
            'upt'
           )


starttime = time.time()


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([name(o) for o in Bus.objs]))


def thr(event):
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith("<_"):
            continue
        obj = Object()
        update(obj, vars(thread))
        if getattr(obj, "sleep", None):
            uptime = obj.sleep - int(time.time() - obj.state["latest"])
        else:
            uptime = int(time.time() - starttime)
        result.append((uptime, thread.name))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s/%s" % (txt, elapsed(uptime)))
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads running")


def upt(event):
    event.reply(elapsed(time.time()-starttime))
