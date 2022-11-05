# This file is placed in the Public Domain.
# pylint: disable=R,C,W,C0302


"""object programming runtime


SYNOPSIS

 opr [-c] [-i] [-r]
 opr <cmd> [key=value] [key==value]

INSTAL

 pip3 install opr --upgrade --force-reinstall

DESCRIPTION

With opr your can have the commands of a irc bot available on your cli.
Instead of having to join a irc channel and give commands to your bot, you
can run these commands on your shell.

opr stores it's data on disk where objects are time versioned and the
last version saved on disk is served to the user layer. Files are JSON dumps
that are read-only so thus should provide (disk) persistence. Paths carry the
type in the path name what makes reconstruction from filename easier then
reading type from the object.


AUTHOR

Bart Thate


COPYRIGHT

opr is placed in the Public Domain. No Copyright, No License.

"""

__version__ = "104"


## imports


import inspect
import os


from .obj import Class, Default, Wd
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


def savepid():
    k = open(os.path.join(Wd.workdir, 'opr.pid'), "w", encoding='utf-8')
    k.write(str(os.getpid()))
    k.close()


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

