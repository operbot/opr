# This file is placed in the Public Domain.


"commands"


import threading
import time


from opr.hdl import Command
from opr.obj import Class, Object, find, fntime, items, save, update
from opr.utl import elapsed


starttime = time.time()


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
    event.reply("ok")


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
    event.reply("ok")


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
