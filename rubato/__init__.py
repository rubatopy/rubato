"""
Rubato is a modern 2D game engine for python. Accurate fixed-step physics
simulations, robust scene and sprite management, event listener system and more
all come prepackaged.

Fundamentally, Rubato is built developer-focused. From intricate rigidbody
simulations to 2D games, Rubato streamlines development for beginners and the
poweruser. And all that finally with some legible documentation.


Note:
    Every single class can be accessed through the top level or through the full
    module path.

Attributes:
    game (Game): The global game class that can be accessed anywhere.
        Initialized when :meth:`rubato.init()` is called.
"""
import warnings

# pylint: disable=wrong-import-position
warnings.simplefilter("ignore", UserWarning)

import sdl2
from rubato.game import Game
from rubato.utils import Math, Display, Vector, Time, Color, Defaults
from rubato.utils.error import *
from rubato.radio import Radio
from rubato.classes import SceneManager, Scene, Camera, Sprite, Image
from rubato.classes import RigidBody, Animation, Component, Polygon, Rectangle, Circle, SAT, Hitbox, Group
import rubato.input as Input
from rubato.sound import Sound

warnings.simplefilter("default", UserWarning)

# This variable tells python which things are included in the library.
# Apparently just importing them isn't enough.
__all__ = [
    "Math",
    "Display",
    "Vector",
    "Time",
    "Polygon",
    "Rectangle",
    "Circle",
    "SAT",
    "Color",
    "Error",
    "IdError",
    "SideError",
    "DuplicateComponentError",
    "ComponentNotAllowed",
    "SceneManager",
    "Scene",
    "Camera",
    "Radio",
    "Sprite",
    "Image",
    "RigidBody",
    "Input",
    "Defaults",
    "Sound",
    "Animation",
    "Component",
    "Hitbox",
    "Group",
    "Game",
]


def init(options: dict = {}):
    """
    Initializes rubato.

    Args:
        options: A game config.
                Defaults to the |default| for `Game`.
    """
    sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
    Game.initialized = True

    params = Defaults.game_defaults | options

    Game.background_color = Color(*params["background_color"]) if not isinstance(params["background_color"],
                                                                                 Color) else params["background_color"]

    Game.foreground_color = Color(*params["foreground_color"]) if not isinstance(params["foreground_color"],
                                                                                 Color) else params["foreground_color"]

    Time.target_fps = params["target_fps"]
    Time.physics_fps = params["physics_fps"]

    flags = (sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI | sdl2.SDL_WINDOW_SHOWN |
             sdl2.SDL_WINDOW_MOUSE_FOCUS | sdl2.SDL_WINDOW_INPUT_FOCUS)

    Display.window = sdl2.ext.Window(params["name"], params["window_size"].to_tuple(), flags=flags)

    Display.renderer = sdl2.ext.Renderer(Display.window,
                                         flags=(sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC),
                                         logical_size=params["res"].to_tuple())

    if params["icon"] != "":
        Display.set_window_icon(params["icon"])

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
            "You have not initialized rubato. Make sure to run rubato.init() right after importing the library")
