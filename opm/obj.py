# This file is placed in the Public Domain.
# pylint: disable=R,C

"""object programming 


The ``op`` package provides an Object class, that allows for save/load
to/from json files on disk. Objects can be searched with database
functions and uses read-only files to improve persistence and a type in
filename for reconstruction. Methods are factored out into functions to
have a clean namespace to read JSON data into.

basic usage is this::

>>> import op
>>> o = op.Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from op import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> from op import Object, save
 >>> o = Object()
 >>> save(o)
 'op.obj.Object/c13c5369-8ada-44a9-80b3-4641986f09df/2021-08-31/15:31:05.717063'

"""


import datetime
import json
import os
import pathlib
import time
import types
import uuid


def __dir__():
    return (
            'Class',
            'Db',
            'Default',
            'Object',
            'ObjectDecoder',
            'ObjectEncoder',
            'Wd',
            'cdir',
            'dump',
            'dumps',
            'edit',
            'find',
            'fns',
            'fntime',
            'hook',
            'items',
            'keys',
            'kind',
            'last',
            'load',
            'loads',
            'match',
            'name',
            'printable',
            'register',
            'save',
            'update',
            'values',
           )


__all__ = __dir__()


class Object:

    __slots__ = ("__dict__", "__fnm__")

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.__fnm__ = os.path.join(
            kind(self),
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            val = args[0]
            if isinstance(val, dict):
                update(self, val)
            elif isinstance(val, Object):
                update(self, vars(val))
        if kwargs:
            self.__dict__.update(kwargs)

    def __delitem__(self, key):
        self.__dict__.__delitem__(key)

    def __getitem__(self, key):
        self.__dict__.__getitem__(key)
          
    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self. __dict__)

    def __setitem__(self, key, value):
        self.__dict__.__setitem__(key, value)


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self):
        Object.__init__(self)
        self.__default__ = ""

    def __getattr__(self, key):
        return self.__dict__.get(key, self.__default__)


def edit(obj, setter):
    for key, value in items(setter):
        register(obj, key, value)


def items(obj):
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    return obj.__dict__.keys()


def kind(obj):
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def name(obj):
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def printable(obj, args="", skip="", plain=False):
    res = []
    keyz = []
    if "," in args:
        keyz = args.split(",")
    if not keyz:
        keyz = keys(obj)
    for key in keyz:
        if key.startswith("_"):
            continue
        if skip:
            skips = skip.split(",")
            if key in skips:
                continue
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    txt = " ".join(res)
    return txt.rstrip()


def register(obj, key, value):
    setattr(obj, key, value)


def update(obj, data):
    for key, value in items(data):
        setattr(obj, key, value)


def values(obj):
    return obj.__dict__.values()


class Db:

    @staticmethod
    def find(otp, selector=None, index=None, timed=None, deleted=False):
        if selector is None:
            selector = {}
        nmr = -1
        res = []
        for fnm in fns(Wd.getpath(otp), timed):
            obj = hook(fnm)
            if deleted and "__deleted__" in obj and obj.__deleted__:
                continue
            if selector and not search(obj, selector):
                continue
            nmr += 1
            if index is not None and nmr != index:
                continue
            res.append(obj)            
        return res

    @staticmethod
    def last(otp, selector=None, index=None, timed=None):
        res =  sorted(Db.find(otp, selector, index, timed), key=lambda x: fntime(x.__fnm__))
        if res:
            return res[-1]

def find(otp, selector=None, index=None, timed=None, deleted=False):
    names = Class.full(otp)
    if not names:
        names = Wd.types(otp)
    result = []
    for nme in names:
        res = Db.find(nme, selector, index, timed, deleted)
        result.extend(res)
    return sorted(result, key=lambda x: fntime(x.__fnm__))


def last(obj):
    ooo = Db.last(kind(obj))
    if ooo:
        update(obj, ooo)


def match(otp, selector=None):
    names = Class.full(otp)
    if not names:
        names = Wd.types(otp)
    for nme in names:
        for item in Db.last(nme, selector):
            return item
    return None


def search(obj, selector):
    res = False
    select = Object(selector)
    for key, value in items(select):
        val = getattr(obj, key)
        if str(value) in str(val):
            res = True
            break
    return res




class ObjectDecoder(json.JSONDecoder):

    def  __init__(self, *args, **kwargs):
        ""
        json.JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        ""
        value = json.loads(s)
        return Object(value)

    def raw_decode(self, s, *args, **kwargs):
        ""
        return json.JSONDecoder.raw_decode(self, s, *args, **kwargs)


class ObjectEncoder(json.JSONEncoder):

    def  __init__(self, *args, **kwargs):
        ""
        json.JSONEncoder.__init__(self, *args, **kwargs)

    def encode(self, o):
        ""
        return json.JSONEncoder.encode(self, o)

    def default(self, o):
        ""
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
            return json.JSONEncoder.default(self, o)
        except TypeError:
            return str(o)

    def iterencode(self, o, *args, **kwargs):
        ""
        return json.JSONEncoder.iterencode(self, o, *args, **kwargs)


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
    fnm = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", fnm)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)
    obj.__fnm__ = fnm


def loads(jss):
    return json.loads(jss, cls=ObjectDecoder)


def save(obj):
    prv = os.sep.join(obj.__fnm__.split(os.sep)[:2])
    obj.__fnm__ = os.path.join(prv, os.sep.join(str(datetime.datetime.now()).split()))
    opath = Wd.getpath(obj.__fnm__)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return obj.__fnm__


class Class:

    cls = {}

    @staticmethod
    def add(clz):
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def all():
        return Class.cls.keys()

    @staticmethod
    def full(oname):
        nme = oname.lower()
        res = []
        for cln in Class.cls:
            if nme == cln.split(".")[-1].lower():
                res.append(cln)
        return res

    @staticmethod
    def get(oname):
        return Class.cls.get(oname, None)

    @staticmethod
    def remove(oname):
        del Class.cls[oname]


class Wd:

    workdir = ""

    @staticmethod
    def get():
        assert Wd.workdir
        return Wd.workdir

    @staticmethod
    def getpath(path):
        return os.path.join(Wd.get(), "store", path)

    @staticmethod
    def set(path):
        Wd.workdir = path

    @staticmethod
    def storedir():
        sdr =  os.path.join(Wd.get(), "store", '')
        if not os.path.exists(sdr):
            cdir(sdr)
        return sdr

    @staticmethod
    def types(oname=None):
        sdr = Wd.storedir()
        res = []
        for fnm in os.listdir(sdr):
            if oname and oname.lower() not in fnm.split(".")[-1].lower():
                continue
            if fnm not in res:
                res.append(fnm)
        return res


Class.add(Object)
Class.add(Default)


def cdir(path):
    if os.path.exists(path):
        return
    if not path.endswith(os.sep):
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    

def fns(otp, timed=None):
    if not otp:
        return []
    assert Wd.workdir
    p = os.path.join(Wd.workdir, "store", otp) + os.sep
    res = []
    d = ""
    for rootdir, dirs, _files in os.walk(p, topdown=False):
        if dirs:
            d = sorted(dirs)[-1]
            if d.count("-") == 2:
                dd = os.path.join(rootdir, d)
                fls = sorted(os.listdir(dd))
                if fls:
                    p = os.path.join(dd, fls[-1])
                    if (
                        timed
                        and "from" in timed
                        and timed["from"]
                        and fntime(p) < timed["from"]
                    ):
                        continue
                    if timed and timed.to and fntime(p) > timed.to:
                        continue
                    res.append(p)
    return sorted(res, key=fntime)


def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    if "." in datestr:
        datestr, rest = datestr.rsplit(".", 1)
    else:
        rest = ""
    t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    if rest:
        t += float("." + rest)
    else:
        t = 0
    return t


def fnclass(path):
    pth = []
    try:
        _rest, *pth = path.split("store")
    except ValueError:
        pass
    if not pth:
        pth = path.split(os.sep)
    return pth[0]
