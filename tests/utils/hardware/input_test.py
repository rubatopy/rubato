"""Test the Input class"""
import pytest
from unittest.mock import Mock
from rubato.utils.error import InitError
from rubato.utils.hardware.rb_input import Input
from rubato import sdl2
# pylint: disable=unused-argument, redefined-outer-name


def test_init():
    with pytest.raises(InitError):
        Input()


### CONTROLLER TESTS ###
@pytest.fixture
def controller():
    c = Mock(sdl2.SDL_Joystick)
    Input._controllers.append(c)
    yield c
    try:
        Input._controllers.remove(c)
    except ValueError:
        pass


def test_update_controllers(controller, monkeypatch: pytest.MonkeyPatch):
    assert Input.controllers == 1

    # detected controllers is the same as the number of known controllers
    numjoys = Mock(return_value=1)
    monkeypatch.setattr(sdl2, "SDL_NumJoysticks", numjoys)
    Input.update_controllers()
    numjoys.assert_called_once()

    # detected controllers is greater than the number of known controllers
    numjoys.reset_mock()
    joystate = Mock()
    monkeypatch.setattr(sdl2, "SDL_JoystickEventState", joystate)
    joyopen = Mock(return_value=controller)
    monkeypatch.setattr(sdl2, "SDL_JoystickOpen", joyopen)
    Input._controllers.remove(controller)
    Input.update_controllers()
    numjoys.assert_called_once()
    joystate.assert_called_once_with(sdl2.SDL_ENABLE)
    joyopen.assert_called_once_with(0)
    assert Input.controllers == 1

    # detected controllers is less than the number of known controllers
    numjoys.reset_mock()
    joyopen.reset_mock()
    joyclose = Mock()
    monkeypatch.setattr(sdl2, "SDL_JoystickClose", joyclose)
    Input._controllers.append(controller)
    Input.update_controllers()
    numjoys.assert_called_once()
    assert joyclose.call_count == 2
    joyclose.assert_called_with(controller)
    joyopen.assert_called_once_with(0)
    assert Input.controllers == 1

    # detected controllers is 0
    numjoys.reset_mock()
    numjoys.return_value = 0
    joyclose.reset_mock()
    joystate.reset_mock()
    Input.update_controllers()
    numjoys.assert_called_once()
    joyclose.assert_called_once_with(controller)
    joystate.assert_called_once_with(sdl2.SDL_DISABLE)


def test_controller_info(controller, monkeypatch: pytest.MonkeyPatch):
    assert Input.controller_name(-1) == ""
    assert Input.controller_axis(-1, 0) == 0
    assert not Input.controller_button(-1, 0)
    assert Input.controller_hat(-1, 0) == 0

    with pytest.raises(IndexError):
        Input.controller_name(1)
    with pytest.raises(IndexError):
        Input.controller_axis(1, 0)
    with pytest.raises(IndexError):
        Input.controller_button(1, 0)
    with pytest.raises(IndexError):
        Input.controller_hat(1, 0)

    joyname = Mock(return_value="test")
    monkeypatch.setattr(sdl2, "SDL_JoystickNameForIndex", joyname)
    joyaxis = Mock(return_value=Input._joystick_max)
    monkeypatch.setattr(sdl2, "SDL_JoystickGetAxis", joyaxis)
    joybutton = Mock(return_value=1)
    monkeypatch.setattr(sdl2, "SDL_JoystickGetButton", joybutton)
    joyhat = Mock(return_value=sdl2.SDL_HAT_UP)
    monkeypatch.setattr(sdl2, "SDL_JoystickGetHat", joyhat)
    assert Input.controller_name(0) == "test"
    joyname.assert_called_once_with(0)
    assert Input.controller_axis(0, 0) == 1
    joyaxis.assert_called_once_with(controller, 0)
    assert Input.controller_button(0, 0)
    joybutton.assert_called_once_with(controller, 0)
    assert Input.translate_hat(Input.controller_hat(0, 0)) == "up"
    joyhat.assert_called_once_with(controller, 0)


def test_axis_centered():
    assert Input.axis_centered(0)
    assert Input.axis_centered(0.0999)
    assert Input.axis_centered(-0.0999)
    assert not Input.axis_centered(1)
    assert not Input.axis_centered(-1)


def test_translate_hat():
    assert Input.translate_hat(sdl2.SDL_HAT_CENTERED) == "center"
    assert Input.translate_hat(sdl2.SDL_HAT_UP) == "up"
    assert Input.translate_hat(sdl2.SDL_HAT_DOWN) == "down"
    assert Input.translate_hat(sdl2.SDL_HAT_LEFT) == "left"
    assert Input.translate_hat(sdl2.SDL_HAT_RIGHT) == "right"
    assert Input.translate_hat(sdl2.SDL_HAT_LEFTUP) == "left up"
    assert Input.translate_hat(sdl2.SDL_HAT_LEFTDOWN) == "left down"
    assert Input.translate_hat(sdl2.SDL_HAT_RIGHTUP) == "right up"
    assert Input.translate_hat(sdl2.SDL_HAT_RIGHTDOWN) == "right down"
    assert Input.translate_hat(9999) == "unknown"


### KEYBOARD TESTS ###
def test_mods():
    vals = [
        "shift",
        "left shift",
        "right shift",
        "alt",
        "left alt",
        "right alt",
        "ctrl",
        "left ctrl",
        "right ctrl",
        "gui",
        "left gui",
        "right gui",
        "numlock",
        "caps lock",
        "altgr",
    ]
    for v in Input._mods.keys():
        assert v in vals


def test_key_pressed(monkeypatch: pytest.MonkeyPatch):
    keyboard_state = Mock(return_value=[True, False, True])
    monkeypatch.setattr(Input, "get_keyboard_state", keyboard_state)
    scancode = Mock(side_effect=[0, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2])
    monkeypatch.setattr(Input, "scancode_from_name", scancode)
    assert Input.key_pressed("a")
    assert not Input.key_pressed("b")
    assert Input.key_pressed("shift")
    assert Input.key_pressed("ctrl")
    assert Input.key_pressed("alt")
    assert Input.key_pressed("gui")
    assert keyboard_state.call_count == 6
    assert scancode.call_count == 11
    scancode.assert_any_call("a")
    scancode.assert_any_call("b")
    scancode.assert_any_call("left shift")
    scancode.assert_any_call("right shift")
    scancode.assert_any_call("left ctrl")
    scancode.assert_any_call("right ctrl")
    scancode.assert_any_call("left alt")
    scancode.assert_any_call("right alt")
    scancode.assert_any_call("left gui")
    scancode.assert_any_call("right gui")

    keyboard_state.reset_mock()
    scancode.reset_mock(side_effect=True)
    scancode.side_effect = [0]
    modstate = Mock(return_value=3)
    monkeypatch.setattr(sdl2, "SDL_GetModState", modstate)
    assert Input.key_pressed("shift", "a")
    assert not Input.key_pressed("ctrl", "b")
    assert modstate.call_count == 2
    scancode.assert_called_once_with("a")
    assert keyboard_state.call_count == 2


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


### MOUSE TESTS ###

### OTHER TESTS ###
