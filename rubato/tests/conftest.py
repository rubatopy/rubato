"""Global Fixtures needed in multiple tests"""
import os
from dotenv import load_dotenv
import pytest
import sdl2
import sdl2.ext

import rubato
from rubato.utils.vector import Vector


@pytest.fixture(scope="module")
def sdl():
    """Initialize SDL2"""
    sdl2.SDL_ClearError()
    res = sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO | sdl2.SDL_INIT_TIMER)
    assert sdl2.SDL_GetError() == b""
    assert res == 0
    yield
    sdl2.SDL_Quit()


@pytest.fixture()
def rub():
    """Initialize Rubato"""
    load_dotenv("rubato/tests/tests.env")

    rubato.init(
        name=os.getenv("WINDOW_NAME"),
        window_size=Vector(int(os.getenv("WINDOW_X")), int(os.getenv("WINDOW_Y"))),
        res=Vector(int(os.getenv("RES_X")), int(os.getenv("RES_Y"))),
        hidden=True,
        window_pos=Vector(int(os.getenv("WINDOW_POS_X")), int(os.getenv("WINDOW_POS_Y"))),
    )
    yield
    sdl2.sdlttf.TTF_Quit()
    sdl2.SDL_Quit()
    rubato.Game.initialized = False
