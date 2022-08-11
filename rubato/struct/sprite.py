"""
A sprite is a class that handles rendering of images.
"""
from __future__ import annotations

import sdl2, sdl2.ext

from .. import get_path, Display, Vector, Game


class Sprite:
    """
    A sprite is a class that handles rendering of images independent of Game Objects.

    Args:
        rel_path: The relative path to the image.
        rotation: The rotation of the image. Defaults to 0.
        scale: The scale of the image. Defaults to Vector(1, 1).
    """

    def __init__(
        self,
        rel_path: str,
        rotation: float = 0,
        scale: Vector = Vector(1, 1),
    ):
        self.image: sdl2.SDL_Surface | str = ""
        """The image that is rendered. This is an SDL_Surface or a string in the surface hasn't been set yet."""
        self.tx: sdl2.ext.Texture | str = ""
        """The generated sprite texture. This is an empty string if it hasn't been set yet."""

        if rel_path != "":
            try:
                self.image = sdl2.ext.load_img(rel_path, False)
            except OSError:
                self.image = sdl2.ext.load_img(get_path(rel_path), False)
            except sdl2.ext.SDLError as e:
                fname = rel_path.replace("\\", "/").split("/")[-1]
                raise TypeError(f"{fname} is not a valid image file") from e

            self.generate_tx()

        self.rotation = rotation
        """The clockwise rotation of the sprite."""
        self.scale = scale
        """The scale of the sprite."""

    def true_scale(self):
        """Gets the scale of the sprite in accordance to camera zoom."""
        return self.scale * Game.camera.zoom

    def get_size(self) -> Vector:
        """
        Gets the current size of the image.

        Returns:
            The size of the image
        """
        tx_size = self.tx.size
        true_scale = self.true_scale()
        return Vector(tx_size[0] * true_scale.x, tx_size[1] * true_scale.y)

    def get_size_original(self) -> Vector:
        """
        Gets the original size of the image.

        Returns:
            Vector: The original size of the image.
        """
        return Vector(self._original.w, self._original.h)

    def generate_tx(self):
        """Regenerates the texture from the surface."""
        self.tx = sdl2.ext.Texture(Display.renderer, self.image)

    def delete(self):
        """Deletes the sprite"""
        self.tx.destroy()
        sdl2.SDL_FreeSurface(self.image)
        self.image = None
        self.tx = None

    def clone(self):
        """
        Creates a clone of the sprite.
        """
        s = Sprite(
            "",
            self.rotation,
            self.scale,
        )
        # pylint: disable=protected-access
        if self.image != "":
            s.image = Display.clone_surface(self.image)
            s.generate_tx()
        return s
