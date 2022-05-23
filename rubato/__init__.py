"""
rubato is a modern 2D game engine for python. Accurate fixed-step physics
simulations, robust scene and game object management, event listener system and more
all come prepackaged.

Fundamentally, rubato is built developer-focused. From intricate rigidbody
simulations to 2D games, rubato streamlines development for beginners and the
poweruser. And all that finally with some legible documentation.
"""

# pylint: disable=wrong-import-position
from warnings import simplefilter
from importlib.resources import files
import os, sys
from pathlib import Path

# Sets the sdl path to the proper rubato sdl directory, from now on all sdl imports will be relative to this directory.
if sys.platform.startswith("darwin"):
    if os.uname().machine == "arm64":
        os.environ["PYSDL2_DLL_PATH"] = str(Path(__file__).parent / "static/dll/mac/silicon")
    else:
        os.environ["PYSDL2_DLL_PATH"] = str(Path(__file__).parent / "static/dll/mac/intel")
if sys.platform.startswith("win32"):
    os.environ["PYSDL2_DLL_PATH"] = str(Path(__file__).parent / "static/dll/windows")

simplefilter("ignore", UserWarning)

import sdl2, sdl2.sdlttf, sdl2.ext

simplefilter("default", UserWarning)

from .utils import *
from .game import Game
from .classes import *


def init(options: dict = {}):
    """
    Initializes rubato.

    Args:
        options: A game config.
                Defaults to the :ref:`Game defaults <gamedef>`.
    """
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

    Game.initialized = True

    params = Defaults.game_defaults | options

    Game.border_color = Color(*params["border_color"]
                             ) if not isinstance(params["border_color"], Color) else params["border_color"]

    Game.background_color = Color(*params["background_color"]
                                 ) if not isinstance(params["background_color"], Color) else params["background_color"]

    Time.target_fps = params["target_fps"]
    Time.capped = Time.target_fps != 0
    if Time.capped:
        Time.normal_delta = 1000 / params["target_fps"]
    Time.physics_fps = params["physics_fps"]
    Time.fixed_delta = 1000 / params["physics_fps"]

    flags = (
        sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI | sdl2.SDL_WINDOW_MOUSE_FOCUS |
        sdl2.SDL_WINDOW_INPUT_FOCUS
    )

    if params["hidden"]:
        flags |= sdl2.SDL_WINDOW_HIDDEN
    else:
        flags |= sdl2.SDL_WINDOW_SHOWN

    params["window_size"] = params["window_size"].to_int()
    params["res"] = params["res"].to_int()

    Display.window = sdl2.ext.Window(
        params["name"], params["window_size"].to_tuple(),
        params["window_pos"].to_tuple() if params["window_pos"] else None, flags
    )

    Display.renderer = sdl2.ext.Renderer(
        Display.window, flags=(sdl2.SDL_RENDERER_ACCELERATED), logical_size=params["res"].to_tuple()
    )

    if params["icon"]:
        Display.set_window_icon(params["icon"])
    else:
        Display.set_window_icon(files("rubato.static.png").joinpath("logo_filled.png"))

    Game.debug_font = Font(
        {
            "size": Display.res.y // 40 if Display.res.y > 0 else 1,
            "font": "PressStart",
            "color": Color(0, 255, 0)
        }
    )

    Game.scenes = SceneManager


def begin():
    """
    Starts the main game loop.

    Raises:
        RuntimeError: rubato has not been initialized before calling.
    """
    if Game.initialized:
        Game.scenes.setup()
        Game.constant_loop()
    else:
        raise RuntimeError(
            "You have not initialized rubato. Make sure to run rubato.init() right after importing the library"
        )


def end():
    """
    Quit the game and close the python process. You can also do this by setting ``Game.state`` to ``Game.STOPPED``.
    """
    Game.state = Game.STOPPED


def pause():
    """
    Pause the game. You can also do this by setting ``Game.state`` to ``Game.PAUSED``.
    """
    Game.state = Game.PAUSED


def resume():
    """
    Resumes the game. You can also do this by setting ``Game.state`` to ``Game.RUNNING``.
    """
    Game.state = Game.RUNNING
