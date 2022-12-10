# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0703,W0201,R0902,R0903,W0613,R0201


"handler"


import inspect
import os
import queue
import sys
import threading
import time


from opr.object import Class, Default, Object, register, spl, update


def __dir__():
    return (
            'Bus',
            'Cfg',
            'Client',
            'Command',
            'Parsed',
            'Event',
            'Handler',
            'command',
            'parse',
            'scan',
            'scandir',
            'scanpkg',
            'skip',
            'starttime',
            'wait'
           )


__all__ = __dir__()


Cfg = Default()
starttime = time.time()


class Bus(Object):

    objs = []

    @staticmethod
    def add(obj):
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
        if bot.cbs:
            bot.say(channel, txt)


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
            func(evt)
            evt.show()
        evt.ready()



class Handler(Object):

    cbs = Object()

    def dispatch(self, event):
        func = getattr(Handler.cbs, event.type, None)
        if not func:
            event.ready()
            return
        event.starttime = time.time()
        func(event)

    def loop(self):
        while 1:
            self.dispatch(self.poll())

    def poll(self):
        raise NotImplementedError("poll")

    def register(self, typ, cbs):
        setattr(Handler.cbs, typ, cbs)

    def start(self):
        self.loop()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("event", Command.handle)
        Bus.add(self)

    def announce(txt):
        self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        self.raw(txt)


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
        self.result = []
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def error(self):
        pass

    def done(self):
        Bus.say(self.orig, self.channel, "ok")

    def ready(self):
        self.__ready__.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self.__ready__.wait()


def command(cli, txt, event=None):
    evt = (event() if event else Event())
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.dispatch(evt)
    evt.wait()
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
    if "w" in prs.opts:
        prs.wait = True
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


def scandir(path, func, mods=None, init=False):
    res = []
    if mods == None:
        mods = ""
    if not os.path.exists(path):
        return res
    for fnm in os.listdir(path):
        if skip(fnm, mods):
            continue            
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        try:
            pname = fnm.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = fnm.split(os.sep)[-1][:-3]
        path2 = os.path.join(path, fnm)
        res.append(func(pname, mname, path2, init))
    return res


def scanpkg(pkg, func, mods=None, init=False):
    if mods is None:
        mods = ""
    scandir(pkg.__path__[0], func, mods, init)


def skip(name, names):
    for nme in spl(names):
       if nme in name:
           return False
    return True


def wait():
    while 1:
        try: 
            time.sleep(1.0)
        except Exception as ex:
            threading.interrupt_main()
