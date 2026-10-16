import sys
import unittest
import weakref

from parameterized import parameterized_class


class TestWeakrefSlots(unittest.TestCase):
    def test_parameterized_class_inherits_weakref_slot(self):
        class Template(object):
            __slots__ = ("__weakref__",)

        namespace = sys.modules[Template.__module__].__dict__
        name = "_ParameterizedWeakrefCase"
        missing = object()
        previous = namespace.get(name, missing)
        try:
            parameterized_class(
                [{"value": 7}], class_name_func=lambda cls, index, params: name
            )(Template)
            instance = namespace[name]()
            self.assertIsInstance(instance, Template)
            self.assertEqual(instance.value, 7)
            self.assertIs(weakref.ref(instance)(), instance)
            self.assertFalse(hasattr(instance, "__dict__"))
        finally:
            if previous is missing:
                namespace.pop(name, None)
            else:
                namespace[name] = previous
