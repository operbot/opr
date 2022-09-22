# This file is placed in the Public Domain.
# pylint: disable=E1101,C0114,C0115,C0116,C0411,R0903,R0904,W0622,W0401,W0614


"object"


import op
import os
import unittest


from op.all import *


Wd.workdir = ".test"


FN = "store/op.obj.Object/2022-04-11/22:40:31.259218"
VALIDJSON = '{"test": "bla"}'


attrs1 = (
            'Class',
            'Db',
            'Default',
            'Object',
            'ObjectDecoder',
            'ObjectEncoder',
            'Wd',
            'edit',
            'dump',
            'dumps',
            'find',
            'format',
            'get',
            'items',
            'iter',
            'keys',
            'last',
            'load',
            'loads',
            'otype',
            'nme',
            'register',
            'save',
            'search',
            'search',
            'update',
            'values'
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
          '__slots__',
          '__stp__',
          '__str__',
          '__subclasshook__',
         )


class TestObject(unittest.TestCase):

    def test_interface(self):
        self.assertTrue(dir(op), attrs1)

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

    def test_otype(self):
        obj = Object()
        self.assertEqual(otype(obj), "op.obj.Object")

    def test_repr(self):
        self.assertTrue(update(Object(),
                               {"key": "value"}).__repr__(), {"key": "value"})

    def test_setattr(self):
        obj = Object()
        obj.__setattr__("key", "value")
        self.assertTrue(obj.key, "value")

    def test_sizeof(self):
        self.assertEqual(Object().__sizeof__(), 32)

    def test_slots(self):
        self.assertEqual(Object().__slots__, (
                                              "__dict__",
                                              "__stp__",
                                             )
                        )

    def test_stp(self):
        obj = Object()
        self.assertTrue("op.obj.Object" in obj.__stp__)

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
        self.assertEqual(format(obj, keys(obj)), "")

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
        self.assertTrue("Object" in fns(Wd.getpath("op.obj.Object"))[0])

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


class Composite(Object):

    def __init__(self):
        super().__init__()
        self.dbs = Db()


Class.add(Composite)


class TestComposite(unittest.TestCase):

    def test_composite(self):
        composite = Composite()
        path = dump(composite, os.path.join(Wd.workdir, "compositetest"))
        composite2 = Composite()
        load(composite2, path)
        self.assertEqual(type(composite2.dbs), Db)


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
