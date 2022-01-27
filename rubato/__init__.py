"""Rubato is a clean and efficient game engine.

Rubato is a Python game engine that builds off of PyGame to make a cleaner and
more efficient game engine. We aim to make game development in Python much
easier than it currently is. Even though we use PyGame in the backend, when
using Rubato, you do not need to ever touch PyGame.

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
from rubato.utils import PMath, classproperty, STATE, Display, Vector, Time, Polygon, Circle, SAT, COL_TYPE, Color, color, Error
from rubato.scenes import SceneManager, Scene, Camera
from rubato.radio import Radio
from rubato.sprite import Sprite, Image, RigidBody, Button, Rectangle, Text, Empty
from rubato.group import Group
import rubato.input as Input
from rubato.game import Game

# This variable tells python which things are included in the library.
# Apparently just importing them isn't enough.
__all__ = [
    "PMath",
    "classproperty",
    "STATE",
    "Display",
    "Vector",
    "Time",
    "Polygon",
    "Circle",
    "SAT",
    "COL_TYPE",
    "Color",
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
    "color",
]

game: Game = None

# TODO Sound manager
# TODO make it so that the 0,0 coordinate is the center the screen
# TODO Y position is up
# TODO update various game parameters live
# TODO window size doesn't update live


def init(options: dict = {}):
    """
    Initializes rubato.

    Args:
        options: A game config.
                Defaults to the :ref:`default game options <defaultgame>`.
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
