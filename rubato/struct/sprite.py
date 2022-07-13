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
        pos: The position to draw the image at. Defaults to Vector(0, 0).
        rotation: The rotation of the image. Defaults to 0.
        scale: The scale of the image. Defaults to Vector(1, 1).
        aa: Whether anti aliasing is turned on. Defaults to True.

    Attributes:
        image: The image that is rendered. This is an SDL_Surface or a string in the surface hasn't been set yet.
        pos: The position of the image.
    """

    def __init__(
        self,
        rel_path: str,
        pos: Vector = Vector(),
        rotation: float = 0,
        scale: Vector = Vector(1, 1),
        aa: bool = True,
    ):
        self.image: sdl2.SDL_Surface | str = ""
        self._original: sdl2.SDL_Surface | str = ""
        self.tx: sdl2.ext.Texture | str = ""

        if rel_path != "":
            try:
                self.image = sdl2.ext.load_img(rel_path, False)
            except OSError:
                self.image = sdl2.ext.load_img(get_path(rel_path), False)
            except sdl2.ext.SDLError as e:
                fname = rel_path.replace("\\", "/").split("/")[-1]
                raise TypeError(f"{fname} is not a valid image file") from e

            self._original = Display.clone_surface(self.image)
            self.tx = sdl2.ext.Texture(Display.renderer, self.image)

        self.pos = pos
        self._rotation = rotation
        self._scale = scale
        self._aa = aa

        self._changed = True
        self._last_camera_zoom = 1

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
            self.scale.x * self._last_camera_zoom,
            self.scale.y * self._last_camera_zoom,
            int(self.aa),
        ).contents
        self.tx = sdl2.ext.Texture(Display.renderer, self.image)

    def get_size(self) -> Vector:
        """
        Gets the current size of the image.

        Returns:
            The size of the image
        """
        self._update_rotozoom()
        if self.image.w == self._original.w and self.image.h == self._original.h:
            return Vector(self.image.w, self.image.h) * self.scale
        return Vector(self.image.w, self.image.h)

    def get_size_original(self) -> Vector:
        """
        Gets the original size of the image.

        Returns:
            Vector: The original size of the image.
        """
        return Vector(self._original.w, self._original.h)

    def update(self):
        """Updates the rotozoom of the sprite if any changes were made."""
        if self._changed or self._last_camera_zoom != Game.camera.zoom:
            self._last_camera_zoom = Game.camera.zoom
            self._changed = False

            self._update_rotozoom()

    def delete(self):
        """Deletes the sprite"""
        self.tx.destroy()
        sdl2.SDL_FreeSurface(self.image)
        sdl2.SDL_FreeSurface(self._original)
        self.image = None
        self.tx = None
        self._original = None

    def clone(self):
        """
        Creates a clone of the sprite.
        """
        s = Sprite(
            "",
            self.pos,
            self.rotation,
            self.scale,
            self.aa,
        )
        # pylint: disable=protected-access
        if self.image != "":
            s.image = Display.clone_surface(self.image)
            s._original = Display.clone_surface(self._original)
        s._changed = True
        return s
