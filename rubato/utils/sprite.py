"""
A sprite is a class that handles rendering of images.
"""
from __future__ import annotations

import sdl2, sdl2.ext

from . import get_path, Display, Vector, Draw


class Sprite:
    """
    A sprite is a class that handles rendering of images independent of Game Objects.
    """

    def __init__(
        self,
        rel_path: str,
        pos: Vector = Vector(),
        rotation: float = 0,
        scale: Vector = Vector(1, 1),
        aa: bool = True,
        z_index: int = 0,
    ):
        try:
            self.image: sdl2.SDL_Surface = sdl2.ext.load_img(rel_path, False)
        except OSError:
            self.image = sdl2.ext.load_img(get_path(rel_path), False)
        except sdl2.ext.SDLError as e:
            fname = rel_path.replace("\\", "/").split("/")[-1]
            raise TypeError(f"{fname} is not a valid image file") from e

        self._original = Display.clone_surface(self.image)
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

        self._pos = pos
        self._rotation = rotation
        self._scale = scale
        self._aa = aa

        self.z_index = z_index

        self._changed = True

    @property
    def pos(self) -> Vector:
        """The position of the sprite."""
        return self._pos

    @pos.setter
    def pos(self, new: Vector):
        self._pos = new
        self._changed = True

    @property
    def rotation(self) -> float:
        """The rotation of the sprite."""
        return self._rotation

    @rotation.setter
    def rotation(self, new: float):
        self._rotation = new
        self._changed = True

    @property
    def scale(self) -> Vector:
        """The scale of the sprite."""
        return self._scale

    @scale.setter
    def scale(self, new: Vector):
        self._scale = new
        self._changed = True

    @property
    def aa(self) -> bool:
        """Whether anti-aliasing is enabled."""
        return self._aa

    @aa.setter
    def aa(self, new: bool):
        self._aa = new
        self._changed = True

    def _update_rotozoom(self):
        self.image = sdl2.sdlgfx.rotozoomSurfaceXY(
            self._original,
            -self.rotation,
            # It seems that rotation is counterclockwise, even though we assume clockwise until now.
            # Requires further investigation but is a fix for now.
            self.scale.x,
            self.scale.y,
            int(self.aa),
        ).contents
        self._tx = sdl2.ext.Texture(Display.renderer, self.image)

    def render(self):
        """
        Render the sprite.
        """
        if self._changed:
            self._update_rotozoom()
            self._changed = False

        Draw.texture(self._tx, self.pos, self.z_index)
