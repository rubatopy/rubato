"""A module that contains a component wrappers for Surface and Sprite."""
from __future__ import annotations
from .. import Component, Rectangle
from ... import Surface, Sprite
from .... import Vector, Camera, Draw, Surf, Color


class BaseImage(Component):
    """A base image component. Does nothing on its own. Hidden from the user."""

    def __init__(
        self,
        scale: Vector = Vector(1, 1),
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
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
    def aa(self) -> bool:
        """Whether the raster is anti-aliased."""
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

        if self.gameobj.rotation != self._go_rotation:
            self._go_rotation = self.gameobj.rotation
            self.surf.rotation = self.gameobj.rotation + self.rot_offset

        Draw.queue_surf(self.surf, self.gameobj.pos + self.offset, self.true_z, camera)

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
        rot_offset: float = 0,
        aa: bool = False,
        z_index: int = 0,
    ):
        super().__init__(scale, offset, rot_offset, aa, z_index)
        self.surf: Surface = Surface(width, height, scale, rot_offset, aa)

    def clear(self):
        """
        Clears the surface.
        """
        self.surf.clear()

    def draw_point(self, pos: Vector, color: Color = Color.black):
        """
        Draws a point on the image.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
        """
        self.surf.draw_point(pos, color)

    def draw_line(self, start: Vector, end: Vector, color: Color = Color.black):
        """
        Draws a line on the image.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            width: The width of the line. Defaults to 1.
        """
        self.surf.draw_line(start, end, color)

    def draw_rect(self, top_left: Vector, dims: Vector, border: Color = Color.black, fill: Color | None = None):
        """
        Draws a rectangle on the image.

        Args:
            top_left: The top left corner of the rectangle.
            dims: The dimensions of the rectangle.
            border: The border color of the rectangle. Defaults to black.
            fill: The fill color of the rectangle. Set to None for no fill. Defaults to None.
        """
        self.surf.draw_rect(top_left, dims, border, fill)

    def draw_circle(self, center: Vector, radius: int, border: Color = Color.black, fill: Color | None = None):
        """
        Draws a circle on the image.

        Args:
            center: The center of the circle.
            radius: The radius of the circle.
            border: The border color of the circle. Defaults to black.
            fill: The fill color of the circle. Set to None for no fill. Defaults to None.
        """
        self.surf.draw_circle(center, radius, border, fill)

    def draw_poly(self, points: list[Vector | tuple[int, int]], border: Color = Color.black):
        """
        Draws a polygon on the image.

        Args:
            points: The points of the polygon.
            border: The border color of the polygon. Defaults to black.
        """
        self.surf.draw_poly(points, border)

    def get_size(self) -> Vector:
        """
        Gets the current size of the surface.

        Returns:
            The size of the surface
        """
        return self.surf.get_size()

    def get_pixel(self, pos: Vector) -> Color:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        return self.surf.get_pixel(pos)

    def get_pixel_tuple(self, pos: Vector) -> tuple[int, int, int, int]:
        """
        Gets the color of a pixel on the image.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        return self.surf.get_pixel_tuple(pos)

    def switch_color(self, color: Color, new_color: Color):
        """
        Switches a color in the image.

        Args:
            color: The color to switch.
            new_color: The new color to switch to.
        """
        self.surf.switch_color(color, new_color)

    def set_colorkey(self, color: Color):
        """
        Sets the colorkey of the image.
        Args:
            color: Color to set as the colorkey.
        """
        self.surf.set_colorkey(color)

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
        aa: Whether to use anti-aliasing. Defaults to False.
        z_index: The z-index of the image. Defaults to 0.
    """

    def __init__(
        self,
        rel_path: str = "",
        scale: Vector = Vector(1, 1),
        offset: Vector = Vector(0, 0),
        rot_offset: float = 0,
        aa: bool = False,
        z_index: int = 0
    ):
        super().__init__(scale, offset, rot_offset, aa, z_index)
        self.surf: Sprite = Sprite(rel_path, scale=scale, rotation=rot_offset, aa=aa)

    def clone(self) -> Image:
        img = Image("", self.scale, self.offset, self.rot_offset, self.aa, self.z_index)
        img.surf = self.surf.clone()
        return img
