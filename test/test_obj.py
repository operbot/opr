# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0401,W0621,W0614,W1503,R0904,E1101


"object"


import os
import unittest
import _thread


import opr.obj


from opr.obj import *
from opr.hdl import *
from opr.thr import *


Wd.workdir = ".test"


FN = "opr.obj.Object/1dd93ecc467d467c98092239055e926c/2022-04-11/22:40:31.259218"
VALIDJSON = '{"test": "bla"}'


testlock = _thread.allocate_lock()


attrs1 = (
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

attrs2 = (
          '__class__',
          '__delattr__',
          '__delitem__',
          '__dict__',
          '__dir__',
          '__doc__',
          '__eq__',
          '__fnm__',
          '__format__',
          '__ge__',
          '__getattribute__',
          '__getitem__',
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
          '__setitem__',
          '__sizeof__',
          '__slots__',
          '__str__',
          '__subclasshook__',
         )


class TestObject(unittest.TestCase):

    #def setUp(self):
    #    obj = Object()
    #    save(obj)

    def test_match(self):
        mtc = match("opr.obj.Object", {"txt": "test"})
        self.assertTrue(not mtc)

    def test_find(self):
        objs = find("object")
        if objs:
            self.assertTrue("opr.obj.Object" in repr(objs[0]))
        self.assertTrue(True)

    def test_default(self):
        dft = Default()
        self.assertEqual(type(dft), Default)

    def test_name(self):
        obj = Object()
        self.assertEqual(name(obj), "Object")

    def test_decoder(self):
        obj = ObjectDecoder().decode('{"bla": "mekker"}')
        self.assertEqual(obj.bla, "mekker")

    def test_encoder(self):
        obj = Object()
        obj.bla = "mekker"
        jsn = ObjectEncoder().encode(obj)
        self.assertEqual(jsn, '{"bla": "mekker"}')

    def test_interface(self):
        self.assertTrue(dir(opr.obj), attrs1)

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
        self.assertTrue(Object().__module__, "obj")

    def test_kind(self):
        obj = Object()
        self.assertEqual(kind(obj), "opr.obj.Object")

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
        self.assertEqual(printable(obj, keys(obj)), "")

    def test_get(self):
        obj = Object()
        obj.key = "value"
        self.assertEqual(getattr(obj, "key"), "value")

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


class TestDb(unittest.TestCase):

    def test_cdir(self):
        cdir(".test")
        self.assertTrue(os.path.exists(".test"))

    def test_fns(self):
        obj = Object()
        save(obj)
        fnms = fns("opr.obj.Object")
        if fnms:
            self.assertTrue("opr.obj.Object"  in fnms[0])
        self.assertTrue(True)

    def test_hook(self):
        obj = Object()
        obj.key = "value"
        pth = save(obj)
        oobj = hook(pth)
        self.assertEqual(oobj.key, "value")

    def test_last(self):
        oobj = Object()
        oobj.key = "value"
        save(oobj)
        last(oobj)
        self.assertEqual(oobj.key, "value")



class TestPath(unittest.TestCase):

    def test_path(self):
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.259218)


class TestJSON(unittest.TestCase):

    def test_json(self):
        obj = Object()
        obj.test = "bla"
        res = loads(dumps(obj))
        self.assertEqual(res.test, "bla")

    def test_jsondump(self):
        obj = Object()
        obj.test = "bla"
        self.assertEqual(dumps(obj), VALIDJSON)
