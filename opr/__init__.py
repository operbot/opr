# This file is placed in the Public Domain.
# pylint: disable=R,C,W,C0302

"""object programming runtime"""


__version__ = "104"


## imports


import inspect
import os


from .obj import Class, Default
from .evt import Event
from .hdl import Command


def __dir__():
    return (
            'Cfg',
            'command',
            'scan',
            'scandir',
           )


__all__ = __dir__()


## defines


Cfg = Default()


## utility


def command(cli, txt):
    evt = Event()
    evt.parse(txt)
    evt.orig = repr(cli)
    cli.handle(evt)
    return evt


def scan(mod):
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)


def scandir(path, func):
    res = []
    if not os.path.exists(path):
        return res
    for _fn in os.listdir(path):
        if _fn.endswith("~") or _fn.startswith("__"):
            continue
        try:
            pname = _fn.split(os.sep)[-2]
        except IndexError:
            pname = path
        mname = _fn.split(os.sep)[-1][:-3]
        res.append(func(pname, mname))
    return res
