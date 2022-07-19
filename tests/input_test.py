"""Test the Input class"""
from rubato.utils.rb_input import Input


def test_get_name():
    assert Input.get_name(97) == "a"
    assert Input.get_name(49) == "1"


def test_mods_from_code():
    assert Input.mods_from_code(0) == []
    assert Input.mods_from_code(1) == ["shift", "left shift"]
    assert Input.mods_from_code(2) == ["shift", "right shift"]


def test_key_from_name():
    assert Input.key_from_name("a") == 97
    assert Input.key_from_name("1") == 49


def test_scancode_from_name():
    assert Input.scancode_from_name("a") == 4
    assert Input.scancode_from_name("1") == 30
