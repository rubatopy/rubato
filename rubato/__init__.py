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

from rubato.utils import Math, Display, Vector, Time, \
    Color, Error, Defaults
import rubato.game as Game
from rubato.radio import Radio
from rubato.classes import SceneManager, Scene, Camera, Sprite, Image, \
    RigidBody, Animation, Component, Polygon, Rectangle, Circle, \
        SAT, Hitbox, Group
import rubato.input as Input
from rubato.sound import Sound

warnings.simplefilter("default", UserWarning)

STATE = Game.STATE

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
    "STATE",
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
    Game.init(options)


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
            "You have not initialized rubato. Make sure to run rubato.init() right after importing the library"  # pylint: disable=line-too-long
        )
