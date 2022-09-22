# This file is placed in the Public Domain.


"json"


import datetime
import json
import os


from json import JSONDecoder, JSONEncoder


from .cls import Class
from .obj import Object, otype, update
from .utl import cdir, fnclass
from .wdr import Wd


def __dir__():
    return (
            'ObjectDecoder',
            'ObjectEncoder',
            'dump',
            'dumps',
            'load',
            'loads',
            'save'
           )


class ObjectDecoder(JSONDecoder):

    def  __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        value = json.loads(s)
        return Object(value)

    def raw_decode(self, s, *args, **kwargs):
        return JSONDecoder.raw_decode(self, s, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    def  __init__(self, *args, **kwargs):
        JSONEncoder.__init__(self, *args, **kwargs)

    def encode(self, o):
        return JSONEncoder.encode(self, o)

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return o
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)

    def iterencode(self, o, *args, **kwargs):
        return JSONEncoder.iterencode(self, o, *args, **kwargs)


def dump(obj, opath):
    cdir(opath)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            obj.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return opath

def dumps(obj):
    return json.dumps(obj, cls=ObjectEncoder)


def hook(path):
    cname = fnclass(path)
    cls = Class.get(cname)
    if cls:
        obj = cls()
    else:
        obj = Object()
    load(obj, path)
    return obj


def load(obj, opath):
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)


def loads(jss):
    return json.loads(jss, cls=ObjectDecoder)


def save(obj):
    stp = os.path.join(
                       otype(obj),
                       os.sep.join(str(datetime.datetime.now()).split())
                      )
    opath = Wd.getpath(stp)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return stp
