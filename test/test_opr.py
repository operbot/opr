# This file is placed in the Public Domain.


"object"


import json
import os
import unittest


from opr import Object, get, items, keys, register, update, values
from opr import load, otype, save
from opr import edit, printable
from opr import ObjectDecoder, ObjectEncoder
from opr import Wd


Wd.workdir = ".test"


VALIDJSON = '{"test": "bla"}'


attrs1 = (
         'Object',
         'Wd',
         'clear',
         'copy',
         'fromkeys',
         'get',
         'items',
         'keys',
         'matchkey',
         'pop',
         'popitem',
         "register",
         'save',
         'setdefault',
         'update',
         'values',
        )

attrs2 = (
          '__class__',
          '__delattr__',
          '__dict__',
          '__dir__',
          '__doc__',
          '__eq__',
          '__format__',
          '__ge__',
          '__getattribute__',
          '__gt__',
          '__hash__',
          '__init__',
          '__init_subclass__',
          '__iter__',
          '__le__',
          '__len__',
          '__lt__',
          '__module__',
          '__ne__',
          '__new__',
          '__reduce__',
          '__reduce_ex__',
          '__repr__',
          '__setattr__',
          '__sizeof__',
          '__str__',
          '__subclasshook__',
          '__weakref__'
         )


def dumps(name):
    return json.dumps(name, cls=ObjectEncoder)


def loads(name):
    return json.loads(name, cls=ObjectDecoder)


class TestObject(unittest.TestCase):

    def test_constructor(self):
        obj = Object()
        self.assertTrue(type(obj), Object)

    def test__class(self):
        obj = Object()
        clz = obj.__class__()
        self.assertTrue("Object" in str(type(clz)))

    def test_contains(self):
        obj = Object()
        obj.key = "value"
        self.assertTrue("key" in obj)

    def test_delattr(self):
        obj = Object()
        obj.key = "value"
        obj.__delattr__("key")
        self.assertTrue("key" not in obj)

    def test_dict(self):
        obj = Object()
        self.assertEqual(obj.__dict__, {})

    def test_dir(self):
        obj = Object()
        self.assertEqual(
            dir(obj), list(attrs2)
        )

    def test_doc(self):
        obj = Object()
        self.assertEqual(obj.__doc__, None)

    def test_format(self):
        obj = Object()
        self.assertEqual(obj.__format__(""), "{}")

    def test_getattribute(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(obj.__getattribute__("key"), "value")

    def test_hash__(self):
        obj = Object()
        hsj = hash(obj)
        self.assertTrue(isinstance(hsj, int))

    def test_init(self):
        obj = Object()
        self.assertTrue(type(Object.__init__(obj)), Object)

    def test_iter(self):
        obj = Object()
        obj.key = "value"
        self.assertTrue(
            list(obj.__iter__()),
            [
                "key",
            ],
        )

    def test_len(self):
        obj = Object()
        self.assertEqual(len(obj), 0)

    def test_module(self):
        self.assertTrue(Object().__module__, "op")

    def test_otype(self):
        self.assertEqual(otype(Object()), "opr.obj.Object")

    def test_repr(self):
        self.assertTrue(update(Object(),
                               {"key": "value"}).__repr__(), {"key": "value"})

    def test_setattr(self):
        obj = Object()
        obj.__setattr__("key", "value")
        self.assertTrue(obj.key, "value")

    def test_sizeof(self):
        self.assertEqual(Object().__sizeof__(), 32)

    def test_str(self):
        obj = Object()
        self.assertEqual(str(obj), "{}")

    def test_edit(self):
        obj = Object()
        dta = {"key": "value"}
        edit(obj, dta)
        self.assertEqual(obj.key, "value")

    def test_printable(self):
        obj = Object()
        self.assertEqual(printable(obj), "")

    def test_get(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(get(obj, "key"), "value")

    def test_keys(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(keys(obj)),
            [
                "key",
            ],
        )

    def test_items(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(items(obj)),
            [
                ("key", "value"),
            ],
        )

    def test_json(self):
        obj = Object()
        obj.test = "bla"
        oobj = loads(dumps(obj))
        self.assertEqual(oobj.test, "bla")

    def test_jsondump(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)


    def test_load(self):
        obj = Object()
        obj.key = "value"
        pld = save(obj)
        oobj = Object()
        load(oobj, pld)
        self.assertEqual(oobj.key, "value")

    def test_register(self):
        obj = Object()
        register(obj, "key", "value")
        self.assertEqual(obj.key, "value")

    def test_save(self):
        Wd.workdir = ".test"
        obj = Object()
        path = save(obj)
        self.assertTrue(os.path.exists(os.path.join(Wd.workdir, "store", path)))

    def test_update(self):
        obj = Object()
        obj.key = "value"
        oobj = Object()
        update(oobj, obj)
        self.assertTrue(oobj.key, "value")

    def test_values(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(
            list(values(obj)),
            [
                "value",
            ],
        )
