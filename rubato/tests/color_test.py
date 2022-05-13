"""Test the Color Class"""
import pytest
from rubato.utils.color import Color
# pylint: disable=redefined-outer-name


@pytest.fixture(scope="module")
def color():
    """Create a Color object"""
    return Color(0, 127, 255, 255)


def test_init(color):
    """Test the Color class initialization"""
    assert color.r == 0
    assert color.g == 127
    assert color.b == 255
    assert color.a == 255


def test_str(color):
    """Test the Color class string representation"""
    assert str(color) == "Color(r=0, g=127, b=255, a=255)"


def test_eq(color):
    """Test the Color class equality operator"""
    assert color == Color(0, 127, 255, 255)


def test_ne(color):
    """Test the Color class inequality operator"""
    assert color != Color(r=1, g=1, b=1, a=1)


def test_rgba32(color):
    """Test the Color class rgba32 representation"""
    assert color.rgba32 == 0x007FFFFF


def test_darker(color):
    """Test the Color class darker method"""
    c = color.darker(20)
    assert c.r == 0
    assert c.g == 107
    assert c.b == 235
    assert c.a == 255


def test_lighter(color):
    """Test the Color class lighter method"""
    c = color.lighter(20)
    assert c.r == 20
    assert c.g == 147
    assert c.b == 255
    assert c.a == 255


def test_mix_linear(color):
    """Test the Color class mix method"""
    c = color.mix(Color(255, 255, 0, 0), 0.5, "linear")
    assert c.r == 127
    assert c.g == 191
    assert c.b == 127
    assert c.a == 127


def test_mix_mix(color):
    """Test the Color class mix method"""
    c = color.mix(Color(255, 255, 0, 0), 0.5, "mix")
    assert c.r == 186
    assert c.g == 203
    assert c.b == 186
    assert c.a == 127


def test_mix_blend(color):
    """Test the Color class mix method"""
    c = color.mix(Color(255, 255, 0, 0), 0.5, "blend")
    assert c.r == 0
    assert c.g == 127
    assert c.b == 255
    assert c.a == 127


def test_to_tuple(color):
    """Test the Color class to_tuple method"""
    assert color.to_tuple() == (0, 127, 255, 255)


def test_to_hex(color):
    """Test the Color class to_hex method"""
    assert color.to_hex() == "007fffff"


def test_to_hsv(color):
    """Test the Color class to_hsv method"""
    assert color.to_hsv() == (210, 1, 1, 1)


def test_from_rgba32(color):
    """Test the Color class from_rgba32 method"""
    assert Color.from_rgba32(0x007FFFFF) == color


def test_from_hex(color):
    """Test the Color class from_hex method"""
    assert Color.from_hex("007fffff") == color


def test_from_hsv(color):
    """Test the Color class from_hsv method"""
    assert Color.from_hsv(210, 1, 1, 1) == color
