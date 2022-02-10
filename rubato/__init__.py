"""Rubato is a modern game engine for python built around PyGame.
Among a slew of high-demand features such as Runge-Katta physics
simulation (still in alpha), a robust scene manager and radio broadcast
system, Rubato also promises to first and foremost be a developer-focused
library. From intricate physics simulations to 2D games, Rubato streamlines
development to make the process more accessible for beginners and
simultaneously more powerful for advanced users.
And all that, finally, with some actual, legible, documentation.

Rubato is built fundamentally as a PyGame wrapper. However, you can still
utilize underlying PyGame functionality in the case that a feature you
want is not officially supported yet.

Note:
    Every single class can be accessed through the top level or through the full
    module path.

Attributes:
    game (Game): The global game class that can be accessed anywhere.
        Initialized when :meth:`rubato.init()` is called.
"""
from os import environ
# This needs to be set before pygame    pylint: disable=wrong-import-position
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
import sys
# from typeguard.importhook import install_import_hook
# install_import_hook("rubato")
from rubato.utils import Math, STATE, Display, Vector, Time, \
    Polygon, Circle, SAT, COL_TYPE, RGB, Error, Configs
from rubato.scenes import SceneManager, Scene, Camera
from rubato.radio import Radio
from rubato.sprite import Sprite, Group, Image, RigidBody, Button, Rectangle, \
    Text, Empty, Animation
import rubato.input as Input
import rubato.sound as Sound
from rubato.game import Game
Colour = RGB

# This variable tells python which things are included in the library.
# Apparently just importing them isn't enough.
__all__ = [
    "Math",
    "STATE",
    "Display",
    "Vector",
    "Time",
    "Polygon",
    "Circle",
    "SAT",
    "COL_TYPE",
    "RGB",
    "Colour",
    "Error",
    "SceneManager",
    "Scene",
    "Camera",
    "Radio",
    "Sprite",
    "Image",
    "RigidBody",
    "Button",
    "Rectangle",
    "Text",
    "Empty",
    "Group",
    "Input",
    "Game",
    "Configs",
    "Sound",
]

game: Game = None


def init(options: dict = {}):
    """
    Initializes rubato.

    Args:
        options: A game config.
                Defaults to the |default| for `Game`.
    """
    global game
    game = Game(options)


def begin():
    """
    Starts the main game loop.

    Raises:
        RuntimeError: Rubato has not been initialized before calling.
    """
    if game is not None:
        game.start_loop()
    else:
        raise RuntimeError(
            "You have not initialized rubato. Make sure to run rubato.init() right after importing the library"  # pylint: disable=line-too-long
        )
