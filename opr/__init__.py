# This file is placed in the Public Domain.


"""object programming runtime


this module contains a big Object class that provides a clean, no methods,
namespace for json data to be read into. this is necessary so that methods
don't get overwritten by __dict__ updating and, without methods defined on
the object, is easily being updated from a on disk stored json (dict).

basic usage is this:

>>> import opr
>>> o = opr.Object()
>>> o.key = "value"
>>> o.key
'value'

Some hidden methods are provided, methods are factored out into functions
like get, items, keys, register, set, update and values.

load/save from/to disk:

>>> import opr
>>> o = opr.Object()
>>> o.key = "value"
>>> p = opr.save(o)
>>> oo = opr.Object()
>>> opr.load(oo, p)
>>> oo.key
'value'

big Objects can be searched with database functions and uses read-only files
to improve persistence and a type in filename for reconstruction:

'opr.object.Object/11ee5f11bd874f1eaa9005980f9d7a94/2021-08-31/15:31:05.717063'

>>> from opr import Object, save
>>> o = Object()
>>> save(o)  # doctest: +ELLIPSIS
'opr.object.Object/...'

great for giving objects peristence by having their state stored in files.

"""


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


from .handler import *
from .object import *
from .thread import *
from .util import *


def __dir__():
    return (
            'Cfg',
            'Class',
            'Default',
            'Db',
            'Object',
            'Wd',
            'edit',
            'elapsed',
            'find',
            'items',
            'keys',
            'kind',
            'last',
            'locked',
            'match',
            'name',
            'printable',
            'register',
            'save',
            'launch',
            'update',
            'values',
            'write',
           )


__all__ = __dir__()
