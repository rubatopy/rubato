"""Test the Vector class"""
from random import Random
import pytest
from rubato.utils.vector import Vector
from rubato.utils.rb_math import Math
# pylint: disable=redefined-outer-name


@pytest.fixture()
def v1():
    return Vector(1, 1)


@pytest.fixture()
def v34():
    return Vector(3, 4)


def test_init(v1, v34):
    assert v1.x == 1
    assert v1.y == 1
    assert v34.x == 3
    assert v34.y == 4

    with pytest.raises(TypeError):
        Vector(1, "2")  # type: ignore # we are testing the typeerror


def test_mag(v1, v34):
    assert v34.magnitude == 5
    assert v34.mag_sq == 25
    v34.magnitude = 10
    assert v34.magnitude == 10
    assert v34.x == 6
    assert v34.y == 8

    v = Vector()
    assert v.magnitude == 0
    v.magnitude = 0
    assert v.magnitude == 0

    assert v1.mag_sq == 2


def test_sum(v1, v34):
    assert v1.sum() == 2
    assert v34.sum() == 7


def test_angle(v1, v34):
    assert v1.angle == 135
    assert v34.angle == 143.13010235415598


def test_rationalized_mag(v1, v34):
    assert v1.rationalized_mag == "√2"
    assert v1.rationalized_mag_vector == Vector(1, 2)
    assert v1.rationalized_unit == "<1/1√2, 1/1√2>"
    assert v34.rationalized_unit == "<3/5, 4/5>"


def test_normalized(v34):
    normalized = v34.normalized()
    assert normalized.x == pytest.approx(3 / 5)
    assert normalized.y == pytest.approx(4 / 5)
    assert Vector().normalized().x == 0
    assert Vector().normalized().y == 0

    v34.normalize()
    assert normalized == v34


def test_tuple(v1, v34):
    assert v1.to_tuple() == (1, 1)
    assert v34.to_tuple() == (3, 4)


def test_dot(v1, v34):
    assert v1.dot(v34) == 7
    assert v34.dot(v1) == 7


def test_cross(v1, v34):
    assert v1.cross(v34) == 1
    assert v34.cross(v1) == -1


def test_perpendicular(v1, v34):
    assert v1.perpendicular() == Vector(1, -1)
    assert v34.perpendicular(2) == Vector(8, -6)


def test_clamp(v1, v34):
    assert v1.clamp(2, 2) == Vector(2, 2)
    assert v34.clamp(1, 2) == Vector(2, 2)
    assert v34.clamp(Vector(1, 4), Vector(2, 4), True) == Vector(2, 4)


def test_rotate(v1):
    assert v1.rotate(90) == Vector(-1, 1)
    assert v1.rotate(45) == Vector(0, 1.4142135624)


def test_clone(v1, v34):
    v3 = v1.clone()
    assert v3 == v1
    assert v3 is not v1

    v3 = v34.clone()
    assert v3 == v34
    assert v3 is not v34


def test_lerp(v1, v34):
    assert v1.lerp(v34, 0.5) == Vector(2, 2.5)
    assert v34.lerp(v1, 0.5) == Vector(2, 2.5)


def test_round(v1):
    v1 += 0.1111111111
    assert v1.round(1) == Vector(1.1, 1.1)
    assert v1.round(0) == Vector(1, 1)
    assert v1.round(1) == Vector(1.1, 1.1)
    assert v1.round(2) == Vector(1.11, 1.11)


def test_ceil(v1):
    v1 += 0.1111111111
    assert v1.ceil() == Vector(2, 2)


def test_floor(v1):
    v1 += 0.1111111111
    assert v1.floor() == Vector(1, 1)


def test_abs():
    v = Vector(-1, -1)
    assert v.abs() == Vector(1, 1)


def test_dir_to(v1, v34):
    assert v1.dir_to(v34) == Vector(0.5547001962, 0.8320502943)
    assert v34.dir_to(v1) == Vector(-0.5547001962, -0.8320502943)


def test_dist_to(v1, v34):
    assert v1.dist_to(v34) == 3.605551275463989
    assert v34.dist_to(v1) == 3.605551275463989


def test_from_radial():
    assert Vector.from_radial(1, 0) == Vector(0, -1)
    assert Vector.from_radial(1, 90) == Vector(1, 0)
    assert Vector.from_radial(1, 180) == Vector(0, 1)
    assert Vector.from_radial(1, 270) == Vector(-1, 0)
    assert Vector.from_radial(1, 360) == Vector(0, -1)


def test_clamp_mag(v34):
    v = Vector.clamp_magnitude(v34, 2)
    assert v.magnitude == 2


def test_angle_between(v1, v34):
    assert Vector.angle_between(v1, v34) == 8.1301023542


def test_random(monkeypatch):
    random = Random(1)
    monkeypatch.setattr("rubato.utils.vector.random", random)
    v = Vector.rand_unit_vector()
    assert v.x == pytest.approx(0.7474634342)
    assert v.y == pytest.approx(-0.6643029539)


def test_quick_vectors():
    # pylint: disable=comparison-with-callable
    assert Vector.zero() == Vector()
    assert Vector.one() == Vector(1, 1)
    assert Vector.up() == Vector(0, -1)
    assert Vector.down() == Vector(0, 1)
    assert Vector.left() == Vector(-1, 0)
    assert Vector.right() == Vector(1, 0)
    assert Vector.infinity() == Vector(Math.INF, Math.INF)


def test_eq():
    assert Vector(1, 1) == Vector(1, 1)
    assert Vector(1, 1) != Vector(1, 2)
    assert Vector(1, 1) != 1


def test_inequalities():
    assert Vector(1, 1) < Vector(2, 2)
    assert Vector(4, 3) > Vector(2, 2)
    assert Vector(1, 1) <= Vector(1, 1)
    assert Vector(4, 3) >= Vector(1, 1)

    # pylint: disable=expression-not-assigned
    with pytest.raises(TypeError):
        Vector(1, 1) < 2  # type: ignore # we are testing the typeerror
    with pytest.raises(TypeError):
        Vector(4, 3) > 1  # type: ignore # we are testing the typeerror
    with pytest.raises(TypeError):
        Vector(1, 1) <= 1  # type: ignore # we are testing the typeerror
    with pytest.raises(TypeError):
        Vector(4, 3) >= 1  # type: ignore # we are testing the typeerror


def test_str(v1):
    assert str(v1) == "<1.0, 1.0>"
    assert repr(v1) == "Vector(1.0, 1.0)"


def test_math(v1, v34):
    vc = v34.clone()
    vc **= 3
    assert vc == Vector(27, 64)
    assert v34**2 == Vector(9, 16)
    assert v34**v34 == Vector(27, 256)
    with pytest.raises(TypeError):
        v1**set()  # type: ignore # pylint: disable=expression-not-assigned

    vc = v34.clone()
    vc *= 4
    assert vc == Vector(12, 16)
    assert v1 * 2 == Vector(2, 2)
    assert 2 * v1 == Vector(2, 2)
    assert v34 * v1 == Vector(3, 4)
    with pytest.raises(TypeError):
        v1 * set()  # type: ignore # pylint: disable=expression-not-assigned

    vc = v34.clone()
    vc /= 2
    assert vc == Vector(1.5, 2)
    assert v1 / 2 == Vector(0.5, 0.5)
    assert 2 / v1 == Vector(2, 2)
    assert v1 / v34 == Vector(1 / 3, 1 / 4)
    assert (2, 3) / v1 == Vector(2, 3)
    with pytest.raises(TypeError):
        v1 / set()  # type: ignore # pylint: disable=expression-not-assigned
    with pytest.raises(TypeError):
        set() / v1  # type: ignore # pylint: disable=expression-not-assigned

    vc = v34.clone()
    vc //= 2
    assert vc == Vector(1, 2)
    assert v1 // 2 == Vector(0, 0)
    assert 2 // v1 == Vector(2, 2)
    assert v1 // v34 == Vector(0, 0)
    assert (2, 3) // v1 == Vector(2, 3)
    with pytest.raises(TypeError):
        v1 // set()  # type: ignore # pylint: disable=expression-not-assigned
    with pytest.raises(TypeError):
        set() // v1  # type: ignore # pylint: disable=expression-not-assigned

    vc = v34.clone()
    vc += v1
    assert vc == Vector(4, 5)
    assert v1 + v34 == Vector(4, 5)
    assert v1 + 2 == Vector(3, 3)
    assert 2 + v1 == Vector(3, 3)
    with pytest.raises(TypeError):
        v1 + set()  # type: ignore # pylint: disable=expression-not-assigned

    vc = v34.clone()
    vc -= v1
    assert vc == Vector(2, 3)
    assert v1 - v34 == Vector(-2, -3)
    assert 2 - v1 == Vector(1, 1)
    assert v1 - 2 == Vector(-1, -1)
    assert (0, 1) - v1 == Vector(-1, 0)
    with pytest.raises(TypeError):
        v1 - set()  # type: ignore # pylint: disable=expression-not-assigned
    with pytest.raises(TypeError):
        set() - v1  # type: ignore # pylint: disable=expression-not-assigned

    vc = v34.clone()
    vc %= v1
    assert vc == Vector(0, 0)
    assert v34 % 2 == Vector(1, 0)
    assert 5 % v34 == Vector(2, 1)
    assert (5, 6) % v34 == Vector(2, 2)
    with pytest.raises(TypeError):
        v1 % set()  # type: ignore # pylint: disable=expression-not-assigned
    with pytest.raises(TypeError):
        set() % v1  # type: ignore # pylint: disable=expression-not-assigned

    assert -v1 == Vector(-1, -1)

    assert hash(v1) == hash((1, 1))
    assert hash(v34) == hash((3, 4))


def test_iter():
    x = Vector(0, 0)
    x[0] = 1
    x[1] = 2
    assert x.x == 1
    assert x.y == 2

    with pytest.raises(IndexError):
        assert x[2] == 3

    with pytest.raises(IndexError):
        x[2] = 3

    assert list(x) == [1, 2]
