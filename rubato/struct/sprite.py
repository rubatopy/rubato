"""
A sprite is a class that handles rendering of images.
"""
from __future__ import annotations

import sdl2, sdl2.ext

from .. import get_path, Vector, Surf, Display


class Sprite(Surf):
    """
    A sprite is a class that handles rendering of images independent of Game Objects.

    Args:
        rel_path: The relative path to the image.
        rotation: The rotation of the image. Defaults to 0.
        scale: The scale of the image. Defaults to Vector(1, 1).
        aa: Whether or not to use anti-aliasing. Defaults to False.
    """

    def __init__(
        self,
        rel_path: str,
        rotation: float = 0,
        scale: Vector = Vector(1, 1),
        aa: bool = False,
    ):
        super().__init__(rotation=rotation, scale=scale, aa=aa)
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
        s = Sprite("", self.rotation, self.scale, self.aa)
        s.surf = Display.clone_surface(self.surf)
        return s
