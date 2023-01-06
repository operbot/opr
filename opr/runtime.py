# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,C0411,C0413,W0212,R0903,W0201,E0402,W0613


"runtime"


import inspect
import os
import time


from .message import Event, Parsed
from .handler import Command
from .objects import Class, Default, spl, update


def __dir__():
    return (
            "Cfg",
            "Console",
            "boot",
            "command",
            "parse",
            'scanpkg',
            'scandir',
            "wait"
           )


class Config(Default):

    pass


Class.add(Config)


def boot(txt):
    prs = parse(txt)
    if "c" in prs.opts:
        Cfg.console = True
    if "d" in prs.opts:
        Cfg.daemon= True
    if "v" in prs.opts:
        Cfg.verbose = True
    if "w" in prs.opts:
        Cfg.wait = True
    if "x" in prs.opts:
        Cfg.exec = True
    update(Cfg.prs, prs)
    update(Cfg, prs.sets)


def command(cli, txt, event=None):
    evt = (event() if event else Event())
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.handle(evt)
    evt.wait()
    return evt


def include(name, namelist):
    for nme in namelist:
        if nme in name:
            return True
    return False


def listmod(path):
    res = []
    if not os.path.exists(path):
        return res
    for fnm in os.listdir(path):
        if fnm.endswith("~") or fnm.startswith("__"):
            continue
        res.append(fnm.split(os.sep)[-1][:-3])
    return res


def parse(txt):
    prs = Parsed()
    prs.parse(txt)
    update(Cfg.prs, prs)
    return prs


def scan(mod):
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)


def scanpkg(pkg, importer, mods=None):
    path = pkg.__path__[0]
    name = pkg.__name__
    return scandir(path, importer, name)


def scandir(path, importer, pname=None, mods=None):
    res = []
    if pname is None:
        pname = path.split(os.sep)[-1]
    for modname in listmod(path):
        if not modname:
            continue
        if mods and not include(modname, spl(mods)):
            continue
        mname = "%s.%s" % (pname, modname)
        ppath = os.path.join(path, "%s.py" % modname)
        mod = importer(mname, ppath)
        res.append(mod)
    return res


def wait(func=None):
    while 1:
        time.sleep(1.0)
        if func:
            func()


Cfg = Config()
Cfg.prs = Parsed()
