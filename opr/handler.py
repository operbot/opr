# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0703,W0201,R0902,R0903,W0613,R0201,E0402


"handler"


import queue
import threading
import time


from .objects import Object
from .threads import launch


def __dir__():
    return (
            'Bus',
            'Callback',
            'Command',
            'Handler',
           )


__all__ = __dir__()



class Bus(Object):

    objs = []

    @staticmethod
    def add(obj):
        if repr(obj) not in [repr(x) for x in Bus.objs]:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for obj in Bus.objs:
            obj.announce(txt)

    @staticmethod
    def byorig(orig):
        res = None
        for obj in Bus.objs:
            if repr(obj) == orig:
                res = obj
                break
        return res

    @staticmethod
    def say(orig, channel, txt):
        bot = Bus.byorig(orig)
        if bot:
            bot.say(channel, txt)


class Callback(Object):

    cbs = Object()
    errors = []

    @staticmethod
    def register(typ, cbs):
        if typ not in Callback.cbs:
            setattr(Callback.cbs, typ, cbs)

    @staticmethod
    def callback(event):
        func = getattr(Callback.cbs, event.type, None)
        if not func:
            event.ready()
            return
        event.__thr__ = launch(func, event)

    @staticmethod
    def dispatch(event):
        Callback.callback(event)

    @staticmethod
    def get(typ):
        return getattr(Callback.cbs, typ)


class Command(Object):

    cmd = Object()
    errors = []

    @staticmethod
    def add(cmd):
        setattr(Command.cmd, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        return getattr(Command.cmd, cmd, None)

    @staticmethod
    def handle(evt):
        if not evt.isparsed:
            evt.parse()
        func = Command.get(evt.cmd)
        if func:
            try:
                func(evt)
            except Exception as ex:
                evt.__exc__ = ex.with_traceback(ex.__traceback__)
                Command.errors.append(evt)
                evt.ready()
                return None
            evt.show()
        evt.ready()
        return None

    @staticmethod
    def remove(cmd):
        delattr(Command.cmd, cmd)


class Handler(Callback):

    def __init__(self):
        Callback.__init__(self)
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.stopped.clear()
        self.register("event", Command.handle)
        Bus.add(self)

    @staticmethod
    def add(cmd):
        Command.add(cmd)

    def announce(self, txt):
        self.raw(txt)

    def handle(self, event):
        Callback.dispatch(event)

    def loop(self):
        while not self.stopped.set():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put_nowait(event)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def restart(self):
        self.stop()
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def stop(self):
        self.stopped.set()

    def start(self):
        self.stopped.clear()
        self.loop()

    def wait(self):
        while 1:
            time.sleep(1.0)
