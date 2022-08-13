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
        self.uptodate: bool = False
        """
        Whether or not the texture is up to date with the surface.
        Can be set to False to trigger a texture regeneration at the next draw cycle.
        """

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
        self.uptodate = False

    @property
    def aa(self):
        """Whether or not to use anti-aliasing."""
        return self._aa

    @aa.setter
    def aa(self, new: bool):
        self._aa = new
        if self.tx is not None:
            self.tx.set_scale_mode("nearest" if not self.aa else "linear")

    def get_size(self) -> Vector:
        """
        Gets the current size of the image. (Scaled)

        Returns:
            The size of the image
        """
        return Vector(self.surf.w * self.scale.x, self.surf.h * self.scale.y)

    def get_size_raw(self) -> Vector:
        """
        Gets the current size of the image. (Unscaled)

        Returns:
            The size of the image
        """
        return Vector(self.surf.w, self.surf.h)

    def generate_tx(self):
        """Regenerates the texture from the surface."""
        self.tx = sdl2.ext.Texture(Display.renderer, self.surf)
        self.uptodate = True

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
