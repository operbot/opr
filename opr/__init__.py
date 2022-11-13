# This file is placed in the Public Domain.


"""Big Object is a load/saveable python object

This module contains a big Object class that provides a clean, no methods,
namespace for json data to be read into. This is necessary so that methods
don't get overwritten by __dict__ updating and, without methods defined on
the object, is easily being updated from a on disk stored json (dict).

basic usage is this::

 >>> import op
 >>> o = op.Object()
 >>> o.key = "value"
 >>> o.key
 'value'

Some hidden methods are provided, methods are factored out into functions
like get, items, keys, register, set, update and values.

load/save from/to disk::

 >>> import op
 >>> o = op.Object()
 >>> o.key = "value"
 >>> p = op.save(o)
 >>> oo = op.Object()
 >>> op.load(oo, p)
 >>> oo.key
 'value'

Big Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction::

 'op.obj.Object/11ee5f11bd874f1eaa9005980f9d7a94/2021-08-31/15:31:05.717063'

 >>> import op
 >>> o = op.Object()
 >>> op.save(o)  # doctest: +ELLIPSIS
 'op.obj.Object/...'

Great for giving objects peristence by having their state stored in files.

"""


## import


import datetime
import getpass
import inspect
import json
import os
import pathlib
import pwd
import queue
import threading
import time
import types
import uuid


from stat import ST_UID, ST_MODE, S_IMODE


from .obj import *
from .hdl import *
from .thr import *
from .utl import *


from .run import Cfg, from_exception


## define


def __dir__():
    return (
            'Cfg',
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
            'elapsed',
            'find',
            'fns',
            'fntime',
            'from_exception',
            'hook',
            'items',
            'keys',
            'kind',
            'last',
            'launch',
            'load',
            'loads',
            'match',
            'name',
            'printable',
            'register',
            'save',
            'update',
            'values',
            'write'
           )


__all__ = __dir__()
