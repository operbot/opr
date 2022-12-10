# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"debug"


def __dir__():
    return (
            'rse',
           )


def rse(event):
    raise Exception("debug!")
