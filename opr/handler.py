# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0703,W0201,R0902,R0903,W0613,R0201


"handler"


import inspect
import os
import queue
import threading
import time


from .object import Class, Default, Object, register, update
from .thread import launch
from .util import elapsed


def __dir__():
    return (
            'Bus',
            'Callback',
            'Command',
            'Parsed',
            'Event',
            'Handler',
            'command',
            'parse',
            'scan',
            'scandir'
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

    def register(self, typ, cbs):
        if typ not in self.cbs:
            setattr(self.cbs, typ, cbs)

    def callback(self, event):
        func = getattr(self.cbs, event.type, None)
        if not func:
            event.ready()
            return
        try:
            event.__thr__ = launch(func, event)
        except Exception as ex:
            Callback.errors.append(ex)
            event.ready()

    def dispatch(self, event):
        self.callback(event)

    def get(self, typ):
        return getattr(self.cbs, typ)


class Command(Object):

    cmd = Object()

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
            func(evt)
            evt.show()
        evt.ready()

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
        self.dispatch(event)

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
        launch(self.loop)

    def wait(self):
        while 1:
            time.sleep(1.0)


class Parsed(Default):

    def __init__(self):
        Default.__init__(self)
        self.args = []
        self.gets = Default()
        self.isparsed = False
        self.sets = Default()
        self.toskip = Default()
        self.txt = ""

    def parse(self, txt=None):
        self.isparsed = True
        self.otxt = txt or self.txt
        spl = self.otxt.split()
        args = []
        _nr = -1
        for word in spl:
            if word.startswith("-"):
                try:
                    self.index = int(word[1:])
                except ValueError:
                    self.opts = self.opts + word[1:2]
                continue
            try:
                key, value = word.split("==")
                if value.endswith("-"):
                    value = value[:-1]
                    register(self.toskip, value, "")
                register(self.gets, key, value)
                continue
            except ValueError:
                pass
            try:
                key, value = word.split("=")
                register(self.sets, key, value)
                continue
            except ValueError:
                pass
            _nr += 1
            if _nr == 0:
                self.cmd = word
                continue
            args.append(word)
        if args:
            self.args = args
            self.rest = " ".join(args)
            self.txt = self.cmd + " " + self.rest
        else:
            self.txt = self.cmd


class Event(Parsed):


    def __init__(self):
        Parsed.__init__(self)
        self.__ready__ = threading.Event()
        self.__thr__ = None
        self.control = "!"
        self.createtime = time.time()
        self.result = []
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def error(self):
        pass

    def done(self):
        diff = elapsed(time.time()-self.createtime)
        Bus.say(self.orig, self.channel, f'ok {diff}')

    def ready(self):
        self.__ready__.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        for thr in self._thrs:
            thr.join()
        self.__ready__.wait()


def command(cli, txt, event=None):
    evt = (event() if event else Event())
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.handle(evt)
    return evt


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    if "c" in prs.opts:
        prs.console = True
    if "d" in prs.opts:
        prs.debug = True
    if "v" in prs.opts:
        prs.verbose = True
    if "x" in prs.opts:
        prs.exec = True
    update(Cfg, prs)
    return prs


def scan(mod):
    scancls(mod)
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)

def scancls(mod):
    for _key, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)


def scandir(path, func):
    res = []
    if not os.path.exists(path):
        return res
    for fnm in os.listdir(path):
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        try:
            pname = fnm.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = fnm.split(os.sep)[-1][:-3]
        path2 = os.path.join(path, fnm)
        res.append(func(pname, mname, path2))
    return res
