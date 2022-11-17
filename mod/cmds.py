# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,R0903,C0209


"commands"


import threading
import time


from .hdl import Bus, Command
from .obj import Class, Object, find, fntime, save, update
from .thr import name
from .utl import elapsed


starttime = time.time()


def __dir__():
    return (
            'Log',
            'Todo',
            'cmd',
            'flt',
            'log',
            'tdo',
            'thr',
            'upt'
           )


class Log(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ""


Class.add(Log)


class Todo(Log):

    pass


Class.add(Todo)


def cmd(event):
    event.reply(",".join(sorted(Command.cmd)))


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([name(o) for o in Bus.objs]))


def log(event):
    if not event.rest:
        nmr = 0
        for obj in find("log"):
            event.reply("%s %s %s" % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(obj.__fnm__)))
                                     )
            nmr += 1
        return
    obj = Log()
    obj.txt = event.rest
    save(obj)
    event.done()


def tdo(event):
    if not event.rest:
        nmr = 0
        for obj in find("todo"):
            event.reply("%s %s %s" % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(obj.__fnm__))
                                     ))
            nmr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    save(obj)
    event.done()


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
            uptime = int(time.time() - obj.starttime)
        result.append((uptime, thread.getName()))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s/%s" % (txt, elapsed(uptime)))
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads running")


def upt(event):
    event.reply(elapsed(time.time()-starttime))
