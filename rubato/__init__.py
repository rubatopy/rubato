"""
Rubato is a modern 2D game engine for python. Accurate fixed-step physics
simulations, robust scene and game object management, event listener system and more
all come prepackaged.

Fundamentally, Rubato is built developer-focused. From intricate rigidbody
simulations to 2D games, Rubato streamlines development for beginners and the
poweruser. And all that finally with some legible documentation.
"""

# pylint: disable=wrong-import-position
from warnings import simplefilter

simplefilter("ignore", UserWarning)

import sdl2, sdl2.sdlttf

simplefilter("default", UserWarning)

from importlib.resources import files

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
        sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI | sdl2.SDL_WINDOW_SHOWN |
        sdl2.SDL_WINDOW_MOUSE_FOCUS | sdl2.SDL_WINDOW_INPUT_FOCUS
    )

    Display.window = sdl2.ext.Window(params["name"], params["window_size"].to_tuple(), flags=flags)

    Display.renderer = sdl2.ext.Renderer(
        Display.window,
        flags=(sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC),
        logical_size=params["res"].to_tuple()
    )

    if params["icon"] != "":
        Display.set_window_icon(params["icon"])
    else:
        Display.set_window_icon(files("rubato.static.png").joinpath("logo_tiny.png"))

    Game.debug_font = Font(
        {
            "size": Display.res.y // 30 if Display.res.y > 0 else 1,
            "font": "Comfortaa",
            "color": Color(0, 255, 0)
        }
    )

    Game.scenes = SceneManager()


def begin():
    """
    Starts the main game loop.

    Raises:
        RuntimeError: Rubato has not been initialized before calling.
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
