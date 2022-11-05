# This file is placed in the Public Domain.


"trace"


__version__ = "1"


## imports


import os
import traceback


from .obj import name


## utility


def from_exception(exc, txt="", sep=" "):
    """from_exception(exc, txt="", sep=" ")

    return a single lined exception string
    """
    result = []
    for frm in traceback.extract_tb(exc.__traceback__):
        fnm = os.sep.join(frm.filename.split(os.sep)[-2:])
        result.append(f"{fnm}:{frm.lineno}")
    nme = name(exc)
    res = sep.join(result)
    return f"{txt} {res} {nme}: {exc}"
