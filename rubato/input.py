"""
The Input module is the way you collect input from the user.

Attributes:
    key (pygame.key): The pygame key module.
    mouse (pygame.mouse): The pygame mouse module.
"""
import pygame as pg
from rubato.utils import Vector

key = pg.key
mouse = pg.mouse


def is_pressed(char: str) -> bool:
    """
    Checks if a key is pressed.

    Args:
        char (str): The name of the key to check.

    Returns:
        bool: Whether or not the key is pressed.
    """
    return key.get_pressed()[key.key_code(char)]


def mouse_over(center: Vector, dims: Vector = Vector(1, 1)) -> bool:
    """
    Checks if the mouse is inside a rectangle defined by its center
    and dimensions

    Args:
        center (rubato.Vector): The center of the rectangle.
        dims (rubato.Vector, optional): The dimensions of the rectangle.
            Defaults to Vector(1, 1).

    Returns:
        bool: Whether or not the mouse is in the defined rectangle.
    """
    top_left = (center - dims / 2).ceil()
    bottom_right = (center + dims / 2).ceil()
    mouse_pos = Vector(mouse.get_pos()[0], mouse.get_pos()[1])

    return (top_left.x <= mouse_pos.x <= bottom_right.x
            and top_left.y <= mouse_pos.y <= bottom_right.y)
