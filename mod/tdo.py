# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,R0903


"todo"


import time


from opr import Class, Object, elapsed, find, fntime, save



def __dir__():
    return (
            'Todo',
            'todo',
           )


class Todo(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ""


Class.add(Todo)


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
    event.ok()
