"""Low level surface manager."""
from __future__ import annotations
import sdl2, sdl2.ext
from . import Vector, Display


class Surf:
    """This is a low-level surface manager. By itself, it doesn't do much."""

    def __init__(
        self,
        rotation: float = 0,
        scale: Vector = Vector(1, 1),
        aa: bool = False,
    ):
        self.rotation = rotation
        """The clockwise rotation of the sprite."""
        self.scale = scale
        """The scale of the sprite."""
        self._aa = aa

        self._surf: sdl2.SDL_Surface | None = None
        self.tx: sdl2.ext.Texture | None = None
        """(READ ONLY) The generated sprite texture."""

    @property
    def surf(self) -> sdl2.SDL_Surface | None:
        """The surface that is rendered."""
        return self._surf

    @surf.setter
    def surf(self, new: sdl2.SDL_Surface):
        """
        Sets the surface to be rendered.
        """
        self._surf = new
        self.generate_tx()

    @property
    def aa(self):
        """Whether or not to use anti-aliasing."""
        return self._aa

    @aa.setter
    def aa(self, new: bool):
        self._aa = new
        self.tx.set_scale_mode("nearest" if not self.aa else "linear")

    def get_size(self) -> Vector:
        """
        Gets the current size of the image.

        Returns:
            The size of the image
        """
        return Vector(self.tx.size[0] * self.scale.x, self.tx.size[1] * self.scale.y)

    def generate_tx(self):
        """Regenerates the texture from the surface."""
        self.tx = sdl2.ext.Texture(Display.renderer, self.surf)

    def delete(self):
        """Deletes the sprite"""
        self.tx.destroy()
        sdl2.SDL_FreeSurface(self.surf)
        self.surf = None
        self.tx = None

    def clone(self) -> Surf:
        """
        Creates a clone of the sprite.
        """
        s = Surf(
            self.rotation,
            self.scale,
            self.aa,
        )
        s.surf = Display.clone_surface(self.surf)
        return s
