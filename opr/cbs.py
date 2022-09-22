# This file is placed in the Public Domain.


"callbacks"


from .obj import Object


def __dir__():
    return (
            "Callbacks",
           )


class Callbacks(Object):

    cbs = {}

    @staticmethod
    def add(typ, cbs):
        if typ not in Callbacks.cbs:
            Callbacks.cbs[typ] = cbs

    @staticmethod
    def callback(event):
        func = Callbacks.cbs.get(event.type)
        if not func:
            event.ready()
            return
        func(event)

    @staticmethod
    def dispatch(event):
        Callbacks.callback(event)

    @staticmethod
    def get(typ):
        return Callbacks.cbs.get(typ)
