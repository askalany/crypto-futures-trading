
from base.helpers import Singleton


class TestClass(metaclass=Singleton):
    x = 0


def test_singleton_instance():
    instance1 = TestClass()
    instance2 = TestClass()

    assert instance1 is instance2


def test_singleton_variable():
    instance1 = TestClass()
    instance2 = TestClass()

    instance1.x = 1
    assert instance1.x == instance2.x
