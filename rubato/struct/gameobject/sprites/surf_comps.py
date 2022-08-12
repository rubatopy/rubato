"""A module that contains a component wrappers for Surface and Sprite."""
from __future__ import annotations
from .. import Component, Rectangle
from ... import Surface, Sprite
from .... import Vector, Camera, Draw, Surf


class BaseImage(Component):
    """A base image component. Does nothing on it's own"""

    def __init__(
        self,
        scale: Vector = Vector(1, 1),
        offset: Vector = Vector(0, 0),
        rot_offset: Vector = Vector(0, 0),
        aa: bool = False,
        z_index: int = 0,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)
        self.surf: Surf = Surf(rot_offset, scale, aa)

        self.singular = False

        self._rot = rot_offset

        self._go_rotation = 0

    @property
    def scale(self) -> Vector:
        """The scale of the raster."""
        return self.surf.scale

    @scale.setter
    def scale(self, new: Vector):
        self.surf.scale = new

    @property
    def rot_offset(self) -> float:
        """The rotation offset of the raster."""
        return self._rot

    @rot_offset.setter
    def rot_offset(self, new: float):
        self._rot = new
        if self.gameobj:
            self.surf.rotation = self.gameobj.rotation + self.rot_offset
        else:
            self.surf.rotation = self.rot_offset

    @property
    def aa(self) -> bool:
        """Whether or not the raster is anti-aliased."""
        return self.surf.aa

    @aa.setter
    def aa(self, new: bool):
        self.surf.aa = new

    def get_rect(self) -> Rectangle:
        """
        Generates the rectangular bounding box of the raster.

        Returns:
            The Rectangle hitbox that bounds the raster.
        """
        return Rectangle(offset=self.offset, width=self.get_size().x, height=self.get_size().y)

    def get_size(self) -> Vector:
        """
        Gets the current size of the raster.

        Returns:
            The size of the raster
        """
        return self.surf.get_size()

    def update(self):
        if self.hidden:
            return

        if self._go_rotation != self.gameobj.rotation:
            self._go_rotation = self.gameobj.rotation
            self.rot_offset = self.rot_offset

    def draw(self, camera: Camera):
        if self.hidden:
            return

        Draw.queue_surf(
            self.surf, camera.transform(self.gameobj.pos + self.offset - Vector(*self.surf.tx.size) / 2), self.true_z
        )

    def delete(self):
        """Deletes the raster component"""
        self.surf.delete()


class Raster(BaseImage):
    """A raster is a component that contains a surface."""

    def __init__(
        self,
        width: int = 32,
        height: int = 32,
        scale: Vector = Vector(1, 1),
        offset: Vector = Vector(0, 0),
        rot_offset: Vector = Vector(0, 0),
        aa: bool = False,
        z_index: int = 0,
    ):
        super().__init__(scale, offset, rot_offset, aa, z_index)
        self.surf = Surface(width, height, scale, rot_offset, aa)

    def clone(self) -> Raster:
        """
        Clones the current raster.

        Returns:
            The cloned raster.
        """
        r = Raster(
            self.surf.width,
            self.surf.height,
            self.scale,
            self.offset,
            self.rot_offset,
            self.aa,
            self.z_index,
        )
        r.surf = self.surf.clone()
        return r


class Image(BaseImage):
    """
    A component that handles Images.

    Args:
        rel_path: The relative path to the image. Defaults to "".
        scale: The scale of the image. Defaults to Vector(1, 1).
        offset: The offset of the image from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the image. Defaults to 0.
        aa: Whether or not to use anti-aliasing. Defaults to False.
        z_index: The z-index of the image. Defaults to 0.
    """

    def __init__(
        self,
        rel_path: str = "",
        scale: Vector = Vector(1, 1),
        offset: Vector = Vector(0, 0),
        rot_offset: Vector = Vector(0, 0),
        aa: bool = False,
        z_index: int = 0
    ):
        super().__init__(scale, offset, rot_offset, aa, z_index)
        self.surf: Sprite = Sprite(rel_path, scale, rot_offset, aa)

    def clone(self) -> Image:
        img = Image("", self.scale, self.offset, self.rot_offset, self.aa, self.z_index)
        img.surf = self.surf.clone()
        return img
