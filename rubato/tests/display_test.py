"""Test the Display class"""
import os
from unittest.mock import Mock
import pytest

from rubato.utils.display import Display
from rubato.utils.path import get_path
from rubato.utils.vector import Vector


@pytest.mark.rub
def test_properties(rub):
    # pylint: disable=unused-argument, comparison-with-callable
    assert Display.window_size == Vector(int(os.getenv("WINDOW_X")), int(os.getenv("WINDOW_Y")))
    assert Display.res == Vector(int(os.getenv("RES_X")), int(os.getenv("RES_Y")))
    assert Display.window_pos == Vector(
        int(os.getenv("WINDOW_POS_X")),
        int(os.getenv("WINDOW_POS_Y")) + Display.get_window_border_size()[0]
    )
    assert Display.window_name == os.getenv("WINDOW_NAME")

    assert Display.display_ratio == Vector(int(os.getenv("RES_X")), int(os.getenv("RES_Y"))) / \
        Vector(int(os.getenv("WINDOW_X")), int(os.getenv("WINDOW_Y")))

    assert Display.border_size == 0
    assert Display.has_x_border is False
    assert Display.has_y_border is False

    assert Display.window is not None
    assert Display.renderer is not None
    assert Display.format is not None


@pytest.mark.rub
def test_prop_setters(rub):
    # pylint: disable=unused-argument, comparison-with-callable
    Display.window_size = Vector(100, 100)
    assert Display.window_size == Vector(100, 100)
    Display.res = Vector(100, 200)
    assert Display.res == Vector(100, 200)
    assert Display.has_x_border is True
    assert Display.has_y_border is False
    assert Display.border_size == 25

    Display.res = Vector(200, 100)
    assert Display.res == Vector(200, 100)
    assert Display.has_x_border is False
    assert Display.has_y_border is True
    assert Display.border_size == 25

    Display.window_pos = Vector(100, 100)
    assert Display.window_pos == Vector(100, 100)

    Display.window_name = "A new name"
    assert Display.window_name == "A new name"


@pytest.mark.rub
def test_positions(rub):
    # pylint: disable=unused-argument, comparison-with-callable
    res = Vector(int(os.getenv("RES_X")), int(os.getenv("RES_Y")))
    assert Display.top_left == Vector(0, 0)
    assert Display.top_right == Vector(res.x, 0)
    assert Display.bottom_left == Vector(0, res.y)
    assert Display.bottom_right == Vector(res.x, res.y)
    assert Display.top_center == Vector(res.x / 2, 0)
    assert Display.bottom_center == Vector(res.x / 2, res.y)
    assert Display.center_left == Vector(0, res.y / 2)
    assert Display.center_right == Vector(res.x, res.y / 2)
    assert Display.center == Vector(res.x / 2, res.y / 2)
    assert Display.top == 0
    assert Display.bottom == res.y
    assert Display.left == 0
    assert Display.right == res.x


@pytest.mark.rub
def test_window_icon(rub, monkeypatch):
    # pylint: disable=unused-argument
    sdl2_mock = Mock()
    monkeypatch.setattr("rubato.utils.display.sdl2", sdl2_mock)

    Display.set_window_icon("test")
    sdl2_mock.ext.image.load_img.assert_called_once_with(get_path("test"))
    sdl2_mock.SDL_SetWindowIcon.assert_called_once_with(
        Display.window.window, sdl2_mock.ext.image.load_img.return_value
    )


def test_update():
    renderer_mock = Mock()
    Display.renderer = renderer_mock

    class FakeTx:
        size = Vector(100, 100)

    class FakeTx2:
        contents = FakeTx

    Display.update(FakeTx, Vector(0, 0))
    renderer_mock.copy.assert_called_once_with(FakeTx, None, (0, 0, 100, 100))
    renderer_mock.reset_mock()
    Display.update(FakeTx2, Vector(0, 0))
    renderer_mock.copy.assert_called_once_with(FakeTx2, None, (0, 0, 100, 100))


def test_clone(monkeypatch):
    sdl_mock = Mock()
    monkeypatch.setattr("rubato.utils.display.sdl2", sdl_mock)

    # pylint: disable=invalid-name, missing-class-docstring
    class MockSurface:
        pixels = [0, 1]
        w = 1
        h = 1
        pitch = 32

        class format:

            class contents:
                format = 888888

    Display.clone_surface(MockSurface)
    sdl_mock.SDL_CreateRGBSurfaceWithFormatFrom.assert_called_once_with([0, 1], 1, 1, 32, 32, 888888)


@pytest.mark.rub
def test_border_size(rub):
    # pylint: disable=unused-argument
    assert Display.get_window_border_size() == (31, 8, 8, 8)


def test_save_screenshot(monkeypatch):

    with pytest.raises(ValueError):
        Display.save_screenshot("test", extension="gif")

    monkeypatch.setattr("rubato.utils.display.sdl2.SDL_CreateRGBSurfaceWithFormat", lambda *args: None)
    with pytest.raises(RuntimeError):
        Display.save_screenshot("test")

    sdl_free = Mock()
    monkeypatch.setattr("rubato.utils.display.sdl2.SDL_FreeSurface", sdl_free)
    monkeypatch.setattr("rubato.utils.display.sdl2.SDL_CreateRGBSurfaceWithFormat", lambda *args: Mock())
    monkeypatch.setattr("rubato.utils.display.sdl2.SDL_RenderReadPixels", lambda *args: 1)
    monkeypatch.setattr("rubato.utils.display.sdl2.SDL_GetError", lambda: "Fake")
    with pytest.raises(RuntimeError):
        Display.save_screenshot("test")

    assert sdl_free.call_count == 1

    sdl_mock = Mock()
    monkeypatch.setattr("rubato.utils.display.sdl2", sdl_mock)
    sdl_mock.SDL_RenderReadPixels.return_value = 0

    Display.save_screenshot("test", "/", "png", False, 100)
    Display.save_screenshot("test", "/", "jpg", False, 100)
    Display.save_screenshot("test", "/", "bmp", False, 100)

    path = lambda ext: bytes(os.path.join("/", "test" + "." + ext), "utf-8")

    sdl_mock.sdlimage.IMG_SavePNG.assert_called_with(sdl_mock.SDL_CreateRGBSurfaceWithFormat.return_value, path("png"))
    sdl_mock.sdlimage.IMG_SaveJPG.assert_called_with(
        sdl_mock.SDL_CreateRGBSurfaceWithFormat.return_value, path("jpg"), 100
    )
    sdl_mock.SDL_SaveBMP.assert_called_with(sdl_mock.SDL_CreateRGBSurfaceWithFormat.return_value, path("bmp"))

    tmp_path = lambda ext: bytes(get_path(os.path.join("/", "test", "test" + "." + ext)), "utf-8")

    Display.save_screenshot("test", "/", "png", True, 100)
    sdl_mock.sdlimage.IMG_SavePNG.assert_called_with(
        sdl_mock.SDL_CreateRGBSurfaceWithFormat.return_value, tmp_path("png")
    )
