# This file is placed in the Public Domain.


"class"


def __dir__():
    return (
            "Class",
           )


class Class:

    cls = {}

    @staticmethod
    def add(clz):
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def all():
        return Class.cls.keys()

    @staticmethod
    def full(name):
        name = name.lower()
        res = []
        for cln in Class.cls:
            if name == cln.split(".")[-1].lower():
                res.append(cln)
        return res

    @staticmethod
    def get(name):
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name):
        del Class.cls[name]
