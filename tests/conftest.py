"""Global Fixtures needed in multiple tests"""
import pytest

import rubato
import sdl2, sdl2.sdlttf
from rubato.utils.vector import Vector


@pytest.fixture(scope="module")
def sdl():
    """Initialize SDL2"""
    sdl2.SDL_ClearError()
    ret = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_TIMER)
    assert sdl2.SDL_GetError() == b""
    assert ret == 0


@pytest.fixture()
def rub():
    """Initialize Rubato"""
    # pylint: disable=unused-argument
    rubato.init(
        window_size=Vector(200, 100),
        res=Vector(400, 200),
        hidden=True,
        window_pos=Vector(0, 0),
    )
    yield
    rubato.Game._initialized = False
