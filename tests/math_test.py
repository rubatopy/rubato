"""Test the Math class"""
import pytest
from rubato.utils.rb_math import Math


def test_clamp():
    assert Math.clamp(1, 0, 2) == 1
    assert Math.clamp(0, 0, 2) == 0
    assert Math.clamp(2, 0, 2) == 2
    assert Math.clamp(3, 0, 2) == 2
    assert Math.clamp(-1, 0, 2) == 0


def test_sign():
    assert Math.sign(10) == 1
    assert Math.sign(0) == 0
    assert Math.sign(-10) == -1


def test_lerp():
    assert Math.lerp(0, 1, 0.5) == 0.5
    assert Math.lerp(0, 1, 0) == 0
    assert Math.lerp(0, 1, 1) == 1


def test_map():
    assert Math.map(11, 0, 10, 0, 100) == 100  # Test upper bound
    assert Math.map(-1, 0, 10, 0, 100) == 0  # Test lower bound
    assert Math.map(5, 0, 10, 0, 100) == 50  # Test middle
    assert Math.map(6.4, 3, 9, 10, 100) == 61.00000000000001  # Test float


def test_floor():
    assert Math.floor(1.5) == 1
    assert Math.floor(1) == 1
    assert Math.floor(0) == 0
    assert Math.floor(-1) == -1
    assert Math.floor(-1.5) == -2


def test_ceil():
    assert Math.ceil(1.5) == 2
    assert Math.ceil(1) == 1
    assert Math.ceil(0) == 0
    assert Math.ceil(-1) == -1
    assert Math.ceil(-1.5) == -1


def test_is_int():
    assert Math.is_int(1)
    assert Math.is_int(1.0)
    assert not Math.is_int(1.5)
    assert Math.is_int(1.5 + 0.5)


def test_simplify_sqrt():
    assert Math.simplify_sqrt(25) == (5, 1)
    assert Math.simplify_sqrt(50) == (5, 2)
    assert Math.simplify_sqrt(30) == (1, 30)
    assert Math.simplify_sqrt(20) == (2, 5)


def test_simplify():
    assert Math.simplify(1, 4) == (1, 4)
    assert Math.simplify(2, 4) == (1, 2)

    with pytest.raises(TypeError):
        Math.simplify(1, "4")  # type: ignore # We are testing the type error


def test_gen_primes():
    gen = Math.gen_primes()
    assert next(gen) == 2
    assert next(gen) == 3
    assert next(gen) == 5
    assert next(gen) == 7
    assert next(gen) == 11
