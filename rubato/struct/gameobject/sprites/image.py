"""
The image component that renders an image from the filesystem.
"""
from __future__ import annotations
import sdl2

from .. import Component, Rectangle
from ... import Sprite
from .... import Vector, Draw, Camera


class Image(Component):
    """
    A component that handles Images.

    Args:
        rel_path: The relative path to the image. Defaults to "".
        scale: The scale of the image. Defaults to Vector(1, 1).
        flipx: Whether or not to flip the image horizontally. Defaults to False.
        flipy: Whether or not to flip the image vertically. Defaults to False.
        offset: The offset of the image from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the image. Defaults to 0.
        aa: Whether or not to use anti-aliasing. Defaults to False.
        z_index: The z-index of the image. Defaults to 0.
    """

    def __init__(
        self,
        rel_path: str,
        scale: Vector = Vector(1, 1),
        flipx: bool = False,
        flipy: bool = False,
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        aa: bool = False,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)

        if rel_path == "":
            raise ValueError("Image rel_path cannot be an empty string.")

        self._rel_path = rel_path
        self._sprite = Sprite(rel_path, aa=aa)

        self.singular = False

        self._flipx: bool = flipx
        self._flipy: bool = flipy
        self._scale: Vector = scale
        self._resize_scale: Vector = Vector(1, 1)  # This scale factor is changed when the image is resized.
        self._rot = rot_offset

        self._go_rotation = 0
        self._changed = True

    @property
    def image(self) -> sdl2.SDL_Surface:
        """The SDL Surface of the image."""
        return self._sprite.image

    @image.setter
    def image(self, new: sdl2.SDL_Surface):
        self._sprite.image = new
        self._sprite.generate_tx()

    @property
    def scale(self) -> Vector:
        """The scale of the image."""
        return self._scale

    @scale.setter
    def scale(self, new: Vector):
        self._scale = new
        self._changed = True

    @property
    def rot_offset(self) -> float:
        """The rotation offset of the image."""
        return self._rot

    @rot_offset.setter
    def rot_offset(self, new: float):
        self._rot = new
        self._changed = True

    @property
    def flipx(self) -> bool:
        """Whether or not the image is flipped horizontally."""
        return self._flipx

    @flipx.setter
    def flipx(self, new: bool):
        self._flipx = new
        self._changed = True

    @property
    def flipy(self) -> bool:
        """Whether or not the image is flipped vertically."""
        return self._flipy

    @flipy.setter
    def flipy(self, new: bool):
        self._flipy = new
        self._changed = True

    @property
    def aa(self) -> bool:
        """Whether or not the image is anti-aliased."""
        return self._sprite.aa

    @aa.setter
    def aa(self, new: bool):
        self._sprite.aa = new

    def get_rect(self) -> Rectangle:
        """
        Generates the rectangular bounding box of the image.

        Returns:
            The Rectangle hitbox that bounds the image.
        """
        return Rectangle(offset=self.offset, width=self.get_size().x, height=self.get_size().y)

    def get_size(self) -> Vector:
        """
        Gets the current size of the image.

        Returns:
            The size of the image
        """
        return self._sprite.get_size()

    def get_size_original(self) -> Vector:
        """
        Gets the original size of the image.

        Returns:
            Vector: The original size of the image.
        """
        return self._sprite.get_size_original()

    def _update_sprite(self):
        if self.gameobj:
            self._sprite.rotation = -self.gameobj.rotation - self.rot_offset
            self._sprite.scale = Vector(
                (-self.scale.x if self.flipx else self.scale.x) * self._resize_scale.x,
                (-self.scale.y if self.flipy else self.scale.y) * self._resize_scale.y
            )

    def resize(self, new_size: Vector):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        if -1 < new_size.x < 1:
            new_size.x = 1
        if -1 < new_size.y < 1:
            new_size.y = 1

        self._resize_scale = Vector(new_size.x / self.get_size_original().x, new_size.y / self.get_size_original().y)
        self._changed = True

    def update(self):
        if self.hidden:
            return

        if self._changed or self._go_rotation != self.gameobj.rotation:
            self._go_rotation = self.gameobj.rotation
            self._changed = False
            self._update_sprite()

    def draw(self, camera: Camera):
        if self.hidden:
            return

        Draw.queue_sprite(
            self._sprite, camera.transform(self.gameobj.pos + self.offset - Vector(*self._sprite.tx.size) / 2),
            self.true_z
        )

    def delete(self):
        """Deletes the image component"""
        self._sprite.delete()

    def clone(self) -> Image:
        """
        Clones the current image.

        Returns:
            Image: The cloned image.
        """
        new = Image(
            rel_path=self._rel_path,
            offset=self.offset,
            scale=self.scale,
            flipx=self.flipx,
            flipy=self.flipy,
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )
        return new
