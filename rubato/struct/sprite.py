"""
Utility class for rendering images to the screen without using a game object.
"""
from __future__ import annotations

import sdl2, sdl2.ext

from . import Surface
from .. import get_path, Display, Vector


class Sprite(Surface):
    """
    Renders images from your file system without being constrained to a game object.

    Args:
        rel_path: The relative path to the image.
        rotation: The rotation of the image. Defaults to 0.
        scale: The scale of the image. Defaults to (1, 1).
        af: Whether to use anisotropic filtering. Defaults to False.
    """

    def __init__(
        self,
        rel_path: str,
        rotation: float = 0,
        scale: Vector | tuple[float, float] = (1, 1),
        af: bool = False,
    ):
        super().__init__(rotation=rotation, scale=scale, af=af)
        if rel_path != "":
            try:
                self.surf = sdl2.ext.load_img(rel_path, False)
            except OSError:
                self.surf = sdl2.ext.load_img(get_path(rel_path), False)
            except sdl2.ext.SDLError as e:
                fname = rel_path.replace("\\", "/").split("/")[-1]
                raise TypeError(f"{fname} is not a valid image file") from e

            self.generate_tx()

    def clone(self) -> Sprite:
        s = Sprite("", self.rotation, self.scale.clone(), self.af)
        s.surf = Display.clone_surface(self.surf)
        return s
