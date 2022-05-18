"""Test the Color Class"""
import pytest
from rubato.utils.color import Color
from rubato.utils.defaults import Defaults
from random import Random
# pylint: disable=redefined-outer-name


@pytest.fixture()
def color():
    return Color(0, 127, 255, 255)


def test_init(color):
    assert color.r == 0
    assert color.g == 127
    assert color.b == 255
    assert color.a == 255


def test_str(color):
    assert str(color) == "Color(r=0, g=127, b=255, a=255)"


def test_eq(color):
    assert color == Color(0, 127, 255, 255)


def test_ne(color):
    assert color != Color(r=1, g=1, b=1, a=1)


def test_eq_withother(color):
    assert color != Random


def test_rgba32(color):
    assert color.rgba32 == 0x007FFFFF


def test_darker(color):
    c = color.darker(20)
    assert c.r == 0
    assert c.g == 107
    assert c.b == 235
    assert c.a == 255


def test_lighter(color):
    c = color.lighter(20)
    assert c.r == 20
    assert c.g == 147
    assert c.b == 255
    assert c.a == 255


def test_mix_linear(color):
    c = color.mix(Color(255, 255, 0, 0), 0.5, "linear")
    assert c.r == 127
    assert c.g == 191
    assert c.b == 127
    assert c.a == 127


def test_mix_mix(color):
    c = color.mix(Color(255, 255, 0, 0), 0.5, "mix")
    assert c.r == 186
    assert c.g == 203
    assert c.b == 186
    assert c.a == 127


def test_mix_blend(color):
    c = color.mix(Color(255, 255, 0, 0), 0.5, "blend")
    assert c.r == 0
    assert c.g == 127
    assert c.b == 255
    assert c.a == 127


def test_to_tuple(color):
    assert color.to_tuple() == (0, 127, 255, 255)


def test_to_hex(color):
    assert color.to_hex() == "007fffff"


@pytest.mark.parametrize(
    "c, expected",
    [
        (Color(a=0), (0, 0, 0, 0)),
        (Color(r=255), (0, 1, 1, 1)),
        (Color(g=255), (120, 1, 1, 1)),
        (Color(b=255), (240, 1, 1, 1)),
    ],
)
def test_to_hsv(c, expected):
    assert c.to_hsv() == expected


def test_from_rgba32(color):
    assert Color.from_rgba32(0x007FFFFF) == color


def test_from_rgba32_0():
    assert Color.from_rgba32(0) == Color(0, 0, 0, 0)


def test_from_hex(color):
    assert Color.from_hex("007fffff") == color


def test_from_hex_wrong_length():
    with pytest.raises(ValueError):
        Color.from_hex("007")


def test_from_hex_wrong_format():
    with pytest.raises(ValueError):
        Color.from_hex("#007fffff")


def test_from_hsv(color):
    assert Color.from_hsv(210, 1, 1, 1) == color


@pytest.mark.parametrize(
    "test_color, expected",
    [
        (Color.black, Defaults.grayscale_defaults["black"]),
        (Color.white, Defaults.grayscale_defaults["white"]),
        (Color.night, Defaults.grayscale_defaults["night"]),
        (Color.darkgray, Defaults.grayscale_defaults["darkgray"]),
        (Color.gray, Defaults.grayscale_defaults["gray"]),
        (Color.lightgray, Defaults.grayscale_defaults["lightgray"]),
        (Color.snow, Defaults.grayscale_defaults["snow"]),
        (Color.yellow, Defaults.color_defaults["yellow"]),
        (Color.orange, Defaults.color_defaults["orange"]),
        (Color.red, Defaults.color_defaults["red"]),
        (Color.scarlet, Defaults.color_defaults["scarlet"]),
        (Color.magenta, Defaults.color_defaults["magenta"]),
        (Color.purple, Defaults.color_defaults["purple"]),
        (Color.violet, Defaults.color_defaults["violet"]),
        (Color.blue, Defaults.color_defaults["blue"]),
        (Color.cyan, Defaults.color_defaults["cyan"]),
        (Color.turquoize, Defaults.color_defaults["turquoize"]),
        (Color.green, Defaults.color_defaults["green"]),
        (Color.lime, Defaults.color_defaults["lime"]),
    ],
)
def test_colors(test_color, expected):
    assert test_color.r == expected[0]
    assert test_color.g == expected[1]
    assert test_color.b == expected[2]
    assert test_color.a == 255


def test_clear():
    c = Color.clear
    assert c.r == 0
    assert c.g == 0
    assert c.b == 0
    assert c.a == 0


def test_random(monkeypatch):
    random = Random(1)
    monkeypatch.setattr("rubato.utils.color.randint", random.randint)
    c = Color.random
    assert c.r == 68
    assert c.g == 32
    assert c.b == 130
    assert c.a == 255