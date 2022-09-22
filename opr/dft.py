# This file is placed in the Public Domain.


from .obj import Object


def __dir__():
    return (
            "Default",
           )


class Default(Object):

    __slots__ = ("__default__",)

    def __init__(self, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.__default__ = ""

    def __getattr__(self, key):
        val = self.__dict__.get(key, None)
        if val:
            return val
        return self.__default__
