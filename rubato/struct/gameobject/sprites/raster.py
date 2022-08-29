"""Abstract component for manipulating pixels attached to a game object."""
from __future__ import annotations
from .. import Component, Rectangle
from ... import Surface
from .... import Vector, Camera, Draw, Color


class Raster(Component):
    """
    A raster is a component that contains a surface.

    Args:
        width: The width of the Raster. Defaults to 32.
        height: The height of the Raster. Defaults to 32.
        scale: The scale of the Raster. Defaults to (1, 1).
        offset: The offset of the Raster. Defaults to (0, 0).
        rot_offset: The rotation offset of the Raster. Defaults to 0.
        af: Whether to use anisotropic filtering. Defaults to False.
        z_index: The z-index of the Raster. Defaults to 0.
        hidden: Whether to hide the Raster. Defaults to False.
    """

    def __init__(
        self,
        width: int = 32,
        height: int = 32,
        scale: Vector | tuple[float, float] = (1, 1),
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        af: bool = False,
        z_index: int = 0,
        hidden: bool = False,
    ):
        super().__init__(offset, rot_offset, z_index, hidden)
        self.surf: Surface = Surface(width, height, scale, rot_offset, af)
        self.singular = False

        self._go_rotation = 0

    @property
    def scale(self) -> Vector:
        """The scale of the raster."""
        return self.surf.scale

    @scale.setter
    def scale(self, new: Vector):
        self.surf.scale = new

    @property
    def af(self) -> bool:
        """Whether to use anisotropic filtering."""
        return self.surf.af

    @af.setter
    def af(self, new: bool):
        self.surf.af = new

    def get_rect(self) -> Rectangle:
        """
        Generates the rectangular bounding box of the raster.

        Returns:
            The Rectangle hitbox that bounds the raster.
        """
        size = self.get_size()
        return Rectangle(offset=self.offset, width=size.x, height=size.y)

    def merge(self, other: Raster):
        """
        Merges the surface of another component into this one.

        Args:
            other: The other component to merge into this one.
        """
        self.surf.merge(other.surf)

    def update(self):
        if self.gameobj is None:
            return

        if self._go_rotation != self.gameobj.rotation:
            self._go_rotation = self.gameobj.rotation

    def draw(self, camera: Camera):
        if self.gameobj is None:
            return

        if self.gameobj.rotation != self._go_rotation:
            self._go_rotation = self.gameobj.rotation
            self.surf.rotation = self.true_rotation()

        Draw.queue_surf(self.surf, self.true_pos(), self.true_z(), camera)

    def delete(self):
        """Deletes the raster component"""
        self.surf.delete()

    def clear(self):
        """
        Clears the surface.
        """
        self.surf.clear()

    def fill(self, color: Color):
        """
        Fill the surface with a color.

        Args:
            color: The color to fill with.
        """
        self.surf.fill(color)

    def draw_point(self, pos: Vector | tuple[float, float], color: Color = Color.black, blending: bool = True):
        """
        Draws a point on the surface.

        Args:
            pos: The position to draw the point.
            color: The color of the point. Defaults to black.
            blending: Whether to use blending. Defaults to False.
        """
        self.surf.draw_point(pos, color, blending)

    def draw_line(
        self,
        start: Vector | tuple[float, float],
        end: Vector | tuple[float, float],
        color: Color = Color.black,
        aa: bool = False,
        thickness: int = 1,
        blending: bool = True
    ):
        """
        Draws a line on the surface.

        Args:
            start: The start of the line.
            end: The end of the line.
            color: The color of the line. Defaults to black.
            aa: Whether to use anti-aliasing. Defaults to False.
            thickness: The thickness of the line. Defaults to 1.
            blending: Whether to use blending. Defaults to False.
        """
        self.surf.draw_line(start, end, color, aa, thickness, blending)

    def draw_rect(
        self,
        top_left: Vector | tuple[float, float],
        dims: Vector | tuple[float, float],
        border: Color = Color.black,
        border_thickness: int = 1,
        fill: Color | None = None,
        blending: bool = True,
    ):
        """
        Draws a rectangle on the surface.

        Args:
            top_left: The top left corner of the rectangle.
            dims: The dimensions of the rectangle.
            border: The border color of the rectangle. Defaults to black.
            border_thickness: The thickness of the border. Defaults to 1.
            fill: The fill color of the rectangle. Set to None for no fill. Defaults to None.
            blending: Whether to use blending. Defaults to False.
        """
        self.surf.draw_rect(top_left, dims, border, border_thickness, fill, blending)

    def draw_circle(
        self,
        center: Vector | tuple[float, float],
        radius: int,
        border: Color | None = None,
        border_thickness: int = 1,
        fill: Color | None = None,
        aa: bool = False,
        blending: bool = True,
    ):
        """
        Draws a circle on the surface.

        Args:
            center: The center of the circle.
            radius: The radius of the circle.
            border: The border color of the circle. Defaults to None.
            border_thickness: The thickness of the border. Defaults to 1.
            fill: The fill color of the circle. Set to None for no fill. Defaults to None.
            aa: Whether to use anti-aliasing. Defaults to False.
            blending: Whether to use blending. Defaults to False.
        """
        self.surf.draw_circle(center, radius, border, border_thickness, fill, aa, blending)

    def draw_poly(
        self,
        points: list[Vector] | list[tuple[float, float]],
        border: Color | None = None,
        border_thickness: int = 1,
        fill: Color | None = None,
        aa: bool = False,
        blending: bool = True,
    ):
        """
        Draws a polygon on the surface.

        Args:
            points: The points of the polygon.
            border: The border color of the polygon. Defaults to None.
            border_thickness: The thickness of the border. Defaults to 1.
            fill: The fill color of the polygon. Set to None for no fill. Defaults to None.
            aa: Whether to use anti-aliasing. Defaults to False.
            blending: Whether to use blending. Defaults to False.
        """
        self.surf.draw_poly(points, border, border_thickness, fill, aa, blending)

    def get_size(self) -> Vector:
        """
        Gets the current size of the surface.

        Returns:
            The size of the surface
        """
        return self.surf.get_size()

    def get_pixel(self, pos: Vector | tuple[float, float]) -> Color:
        """
        Gets the color of a pixel on the surface.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        return self.surf.get_pixel(pos)

    def get_pixel_tuple(self, pos: Vector | tuple[float, float]) -> tuple[int, int, int, int]:
        """
        Gets the color of a pixel on the surface.

        Args:
            pos: The position of the pixel.

        Returns:
            The color of the pixel.
        """
        return self.surf.get_pixel_tuple(pos)

    def switch_color(self, color: Color, new_color: Color):
        """
        Switches a color in the surface.

        Args:
            color: The color to switch.
            new_color: The new color to switch to.
        """
        self.surf.switch_color(color, new_color)

    def set_colorkey(self, color: Color):
        """
        Sets the colorkey of the surface.
        Args:
            color: Color to set as the colorkey.
        """
        self.surf.set_colorkey(color)

    def set_alpha(self, new: int):
        """
        Sets surface wide alpha.

        Args:
            new: The new alpha. (value between 0-255)
        """
        self.surf.set_alpha(new)

    def get_alpha(self) -> int:
        """
        Gets the surface wide alpha.
        """
        return self.surf.get_alpha()

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
            self.offset.clone(),
            self.rot_offset,
            self.af,
            self.z_index,
        )
        r.surf = self.surf.clone()
        return r
