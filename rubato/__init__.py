"""
This is the top level init file for all of rubato.

Note:
    Every single class can be accessed through the top level or through the full
    module path.

Attributes:
    game (Game): The global game class that can be accessed anywhere.
        Initialized when :meth:`rubato.init()` is called.
"""
import os
# This needs to be set before pygame   pylint: disable=wrong-import-position
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import rubato.static as Static
from rubato.utils import Math, Display, Vector, Time, \
    Color, Error, Configs
from rubato.radio import Radio
from rubato.classes import SceneManager, Scene, Camera, Sprite, Image, \
    RigidBody, Animation, Component, Polygon, Rectangle, Circle, \
        SAT, Hitbox, Group
import rubato.input as Input
import rubato.sound as Sound
import rubato.game as Game

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
    "Configs",
    "Sound",
    "Animation",
    "Component",
    "Static",
    "Hitbox",
    "STATE",
    "Group",
    "Game",
]

radio: Radio = None


def init(options: dict = {}):
    """
    Initializes rubato.

    Args:
        options: A game config.
                Defaults to the |default| for `Game`.
    """
    global radio
    Game.init(options)
    Game.radio = Radio()
    radio = Game.radio


def begin():
    """
    Starts the main game loop.

    Raises:
        RuntimeError: Rubato has not been initialized before calling.
    """
    if Game.is_init:
        Game.scenes.setup()
        Game.constant_loop()
    else:
        raise RuntimeError(
            "You have not initialized rubato. Make sure to run rubato.init() right after importing the library"  # pylint: disable=line-too-long
        )
