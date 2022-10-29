"""Test deprication things"""
import pytest
from rubato.utils.error import RemovedError, deprecated, removed


class Foo:

    def replacement_func(self):
        """Replacement func"""
        pass


def test_depricated():

    @deprecated("1.0.0", "2.0.0", Foo.replacement_func)
    def func():
        """test"""
        return True

    with pytest.deprecated_call():
        assert func()

    assert func.__doc__ is not None
    assert "1.0.0" in func.__doc__
    assert "2.0.0" in func.__doc__
    assert "Foo.replacement_func()" in func.__doc__


def test_removed():

    @removed("1.0.0", Foo.replacement_func)
    def func():
        """test"""
        assert False

    with pytest.raises(RemovedError):
        func()

    assert func.__doc__ is not None
    assert "1.0.0" in func.__doc__
    assert "Foo.replacement_func()" in func.__doc__
