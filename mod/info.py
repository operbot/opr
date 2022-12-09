# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,E1101


"runtime information"


import threading
import time


from opr import Bus, Object, elapsed, name, update


def __dir__():
    return (
            'fleet',
            'threads',
            'uptime'
           )


starttime = time.time()


def fleet(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([name(o) for o in Bus.objs]))


def threads(event):
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        obj = Object()
        update(obj, vars(thr))
        if getattr(obj, "sleep", None):
            upt = obj.sleep - int(time.time() - obj.state["latest"])
        else:
            upt = int(time.time() - obj.starttime)
        result.append((upt, thr.getName()))
    res = []
    for upt, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s/%s" % (txt, elapsed(upt)))
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads running")


def uptime(event):
    event.reply(elapsed(time.time()-starttime))
