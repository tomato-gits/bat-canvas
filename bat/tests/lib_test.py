from unittest import TestCase

from bat.lib import hello_world


class LibTests(TestCase):

    def test_hello_world(t):
        ret = hello_world()
        t.assertEqual(ret, "Hello World!")


class TempTests(TestCase):

    def test_class_property(t):

        class _Prop:
            def __get__(self, _, objtype):
                try:
                    return objtype._property
                except AttributeError:
                    objtype._property = objtype.get_property()
                return objtype._property

            def __set__(self, objtype, value):
                objtype._property = value

        class MetaClass:
            def __init_subclass__(cls, **kwargs):
                cls.prop = _Prop()

            @classmethod
            def get_property(cls):
                return "dynamical property value"

        class SubCls(MetaClass):
            _property = "subby prop"

        t.assertEqual(SubCls.prop, "subby prop")

        class DubSub(MetaClass):
            @classmethod
            def get_property(cls):
                return "dubsub property value"

        t.assertEqual(DubSub.prop, "dubsub property value")

        DubSub.prop = "new value"
        t.assertEqual(DubSub.prop, "new value")
