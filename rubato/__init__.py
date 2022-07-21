"""
rubato is a modern 2D game engine for python. Accurate fixed-step physics
simulations, robust scene and game object management, event listener system and more
all come prepackaged.

Fundamentally, rubato is built developer-focused. From intricate rigidbody
simulations to 2D games, rubato streamlines development for beginners and the
poweruser. And all that finally with some legible documentation.
"""

# pylint: disable=wrong-import-position
from typing import Literal
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
from .struct import *
from .misc import world_mouse, wrap


def init(
    name: str = "Untitled Rubato App",
    res: Vector = Vector(1080, 1080),
    window_size: Vector | None = None,
    pos: Vector | None = None,
    icon: str = "",
    fullscreen: Literal["off", "desktop", "exclusive"] = "off",
    target_fps: int = 0,
    physics_fps: int = 30,
    hidden: bool = False,
):
    """
    Initializes rubato.

    Args:
        name: The title that appears at the top of the window. Defaults to "Untitled Rubato App".
        res: The pixel resolution of the game, cast to int Vector. Defaults to Vector(1080, 1080).
        window_size: The size of the window, cast to int Vector. When not set, defaults to half the resolution.
            This is usually the sweet spot between performance and image quality.
        pos: The position of the window, cast to int Vector. Set to None to let the computer decide.
            Defaults to None.
        icon: The path to the icon that will appear in the window. Defaults to "" (the rubato logo).
        fullscreen: Whether the game should be fullscreen. Can be one of "off", "desktop", or "exclusive".
            Defaults to "off".
        target_fps: The target frames per second. If set to 0, the target fps will be uncapped. Defaults to 0.
        physics_fps: The physics simulation's frames per second. Defaults to 60.
        hidden: Whether or not the window should be hidden. CANNOT BE CHANGED AFTER INIT CALL. Defaults to False.
    """
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

    Game._initialized = True # pylint: disable=protected-access

    Time.target_fps = target_fps
    Time.capped = Time.target_fps != 0
    if Time.capped:
        Time.normal_delta = 1000 / target_fps
    Time.physics_fps = physics_fps
    Time.fixed_delta = 1 / physics_fps

    flags = (
        sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI | sdl2.SDL_WINDOW_MOUSE_FOCUS |
        sdl2.SDL_WINDOW_INPUT_FOCUS
    )

    if hidden:
        flags |= sdl2.SDL_WINDOW_HIDDEN
    else:
        flags |= sdl2.SDL_WINDOW_SHOWN

    pos, change_pos = (pos, True) if pos else (None, False)
    res = res.to_int()
    size = res//2 if not window_size else window_size.to_int()

    Display.window = sdl2.ext.Window(name, size.to_tuple(), pos.to_tuple() if pos else None, flags)

    Display.renderer = sdl2.ext.Renderer(
        Display.window, flags=(sdl2.SDL_RENDERER_ACCELERATED), logical_size=res.to_tuple()
    )

    if change_pos:
        Display.window_pos += Vector(0, Display.get_window_border_size()[0])

    if icon:
        Display.set_window_icon(icon)
    else:
        Display.set_window_icon(files("rubato.static.png").joinpath("logo_filled.png"))

    if fullscreen != "off":
        Display.set_fullscreen(True, fullscreen)

    Game.debug_font = Font(
        size=Display.res.y // 40 if Display.res.y > 0 else 1, font="PressStart", color=Color(0, 255, 0)
    )


def begin():
    """
    Starts the main game loop.

    Raises:
        RuntimeError: rubato has not been initialized before calling.
    """
    if Game._initialized: # pylint: disable=protected-access
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
