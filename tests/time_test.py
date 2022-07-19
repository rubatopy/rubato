"""Test the time class"""
from rubato.utils.rb_time import Time

def test_milli_to_sec():
    assert Time.milli_to_sec(1000) == 1
    assert Time.milli_to_sec(0) == 0
    assert Time.milli_to_sec(-1000) == -1

def test_sec_to_milli():
    assert Time.sec_to_milli(1) == 1000
    assert Time.sec_to_milli(0) == 0
    assert Time.sec_to_milli(-1) == -1000
