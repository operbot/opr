# This file is placed in the Public Domain.


import inspect
import os


from .cls import Class
from .com import Command


def __dir__():
    return (
            "scan",
            "scancls",
            "scancmd",
            "scandir"
           )


def scan(mod):
    scancls(mod)
    scancmd(mod)
    return mod


def scancls(mod):
    for _k, clz in inspect.getmembers(mod, inspect.isclass):
        Class.add(clz)
    return mod


def scancmd(mod):
    for _k, obj in inspect.getmembers(mod, inspect.isfunction):
        if "event" in obj.__code__.co_varnames:
            Command.add(obj)
    return mod


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
