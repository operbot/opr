# This file is placed in the Public Domain.
# pylint: disable=W0622,C0114


"""object programming runtime


The ``opr`` package provides an Object class, that mimics a dict while using
attribute access and provides a save/load to/from json files on disk.
Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction. Methods are
factored out into functions to have a clean namespace to read JSON data into.

basic usage is this::

>>> import opr
>>> o = opr.Object()
>>> o.key = "value"
>>> o.key
>>> 'value'

Objects try to mimic a dictionary while trying to be an object with normal
attribute access as well. hidden methods are provided, the methods are
factored out into functions like get, items, keys, register, set, update
and values.

load/save from/to disk::

>>> from opr import Object, load, save
>>> o = Object()
>>> o.key = "value"
>>> p = save(o)
>>> obj = Object()
>>> load(obj, p)
>>> obj.key
>>> 'value'

great for giving objects peristence by having their state stored in files::

 >>> from opr import Object, save
 >>> o = Object()
 >>> save(o)
 'opr.obj.Object/2021-08-31/15:31:05.717063'

"""


from .bus import Bus
from .cbs import Callbacks
from .cfg import Config
from .clt import Client
from .com import Command, dispatch
from .evt import Event
from .hdl import Handler
from .prs import parse
from .scn import scan, scandir
from .thr import Thread, launch
from .tmr import Timer, Repeater
from .utl import wait
from .cls import Class
from .dbs import Db, all, find, fns, fntime, hook, last, locked
from .dft import Default
from .jsn import ObjectDecoder, ObjectEncoder, dump, dumps, load, loads, save
from .obj import *
from .utl import cdir, elapsed, spl
from .wdr import Wd


def __dir__():
    return (
            'Bus',
            'Callbacks',
            'Class',
            'Client',
            'Command',
            'Config',
            'Db',
            'Default',
            'Event',
            'Handler',
            'Object',
            'ObjectDecoder',
            'ObjectEncoder',
            'Repeater',
            'Thread',
            'Timer',
            'Wd',
            'all',
            'dispatch',
            'delete',
            'dump',
            'dumps',
            'edit',
            'find',
            'format',
            'get',
            'items',
            'keys',
            'launch',
            'last',
            'load',
            'loads',
            'locked',
            'name',
            'otype',
            'parse',
            'register',
            'save',
            'scan',
            'scandir',
            'spl',
            'starttime',
            'update',
            'values',
            'wait'
           )
