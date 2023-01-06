# This file is placed in the Public Domain.
# pylint: disable=E1101,R0903,C0115,C0116


"logging"


import time


from opr.objects import Class, Object, find, fntime, save
from opr.threads import elapsed


def __dir__():
    return (
            'Log',
            'log',
           )


class Log(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ""


Class.add(Log)


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
    event.ok()
