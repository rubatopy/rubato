"""Static image component for game objects."""
from __future__ import annotations
from . import Raster
from ... import Sprite
from .... import Vector


class Image(Raster):
    """
    A component that handles Images.

    Args:
        rel_path: The relative path to the image. Defaults to "".
        scale: The scale of the image. Defaults to (1, 1).
        offset: The offset of the image from the gameobject. Defaults to (0, 0).
        rot_offset: The rotation offset of the image. Defaults to 0.
        af: Whether to use anisotropic filtering. Defaults to False.
        z_index: The z-index of the image. Defaults to 0.
        hidden: Whether the image is hidden or not. Defaults to False.
    """

    def __init__(
        self,
        rel_path: str = "",
        scale: Vector | tuple[float, float] = (1, 1),
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        af: bool = False,
        z_index: int = 0,
        hidden: bool = False
    ):
        super().__init__(0, 0, scale, offset, rot_offset, af, z_index, hidden)
        self.surf: Sprite = Sprite(rel_path, scale=scale, rotation=rot_offset, af=af)

    def clone(self) -> Image:
        img = Image("", self.scale, self.offset.clone(), self.rot_offset, self.af, self.z_index)
        img.surf = self.surf.clone()
        return img
