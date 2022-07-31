"""A text component."""
from __future__ import annotations
from typing import Literal
import sdl2, sdl2.ext

from .. import Component
from .... import Display, Vector, Color, Font, Draw, Camera


class Text(Component):
    """
    A text component subclass. Add this to game objects or UI elements to give them text.

    Args:
        text: The text to display. Defaults to "".
        font: The font to use. Defaults to Font().
        justify: The justification of the text. Defaults to "left".
        anchor: The anchor of the text. The zero vector means it is centered. x component is whether to shift left,
            none, or right (-1, 0, 1). y component is whether to shift top, none, or bottom (-1, 0, 1).
            Defaults to Vector(0, 0).
        width: The width of the text. Defaults to 0.
        offset: The offset of the text from the game object. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the text from the game object. Defaults to 0.
        z_index: The z index of the text. Defaults to 0.
    """

    def __init__(
        self,
        text: str = "",
        font: Font = Font(),
        justify: Literal["left", "center", "right"] = "left",
        anchor: Vector = Vector(0, 0),
        width: int = 0,
        offset: Vector = Vector(),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)
        self._text: str = text
        self._font: Font = font
        self._anchor: Vector = anchor
        self._justify: str = justify
        self._width: int = width
        self._stored_rot: int = 0

        if not self._font:
            self._font = Font()

        self.generate_surface()

    @property
    def text(self) -> str:
        """The text of the Text."""
        return self._text

    @text.setter
    def text(self, new: str):
        self._text = new
        self.generate_surface()

    @property
    def justify(self) -> str:
        """
        The justification of the text.

        Can be one of: ``"left"``, ``"center"``, ``"right"``.
        """
        return self._justify

    @justify.setter
    def justify(self, new: str):
        if new in ["left", "center", "right"]:
            self._justify = new
            self.generate_surface()
        else:
            raise ValueError(f"Justification {new} is not left, center or right.")

    @property
    def anchor(self) -> Vector:
        """
        The anchor vector of the text.

        This controls the position of the text relative to the game object. Is a vector where the x value
        controls the x anchor and the y value controls the y anchor. The values for each can be either -1, 0 or 1. This
        offset the text around the game object center.

        Example:
            An anchor of ``Vector(0, 0)`` will center the text on the game object. An anchor of ``Vector(1, 1)`` will
            move the text so that it's top left corner is at the game object's center.

        Warning:
            Previously was called align.
        """
        return self._anchor

    @anchor.setter
    def anchor(self, new: Vector):
        self._anchor = new

    @property
    def width(self) -> int:
        """The maximum width of the text. Will automatically wrap the text. Use -1 to disable wrapping."""
        return self._width

    @width.setter
    def width(self, new: int):
        self._width = new
        self.generate_surface()

    @property
    def font_object(self) -> Font:
        """The font object of the text."""
        return self._font

    @property
    def font_size(self) -> int:
        """
        The font size.

        Warning:
            Don't set this too high or font smoothing may misbehave on some systems.
        """
        return self._font.size

    @font_size.setter
    def font_size(self, size: int):
        self._font.size = size
        self.generate_surface()

    @property
    def font_color(self) -> Color:
        """The font color."""
        return self._font.color

    @font_color.setter
    def font_color(self, color: Color):
        self._font.color = color
        self.generate_surface()

    def add_style(self, style: str):
        """Add a style to the font (bold, italic, underline, strikethrough, normal)."""
        self._font.add_style(style)
        self.generate_surface()

    def remove_style(self, style: str):
        """Remove a style from a font."""
        self._font.remove_style(style)
        self.generate_surface()

    def generate_surface(self):
        """(Re)generates the surface of the text."""
        self._tx = sdl2.ext.Texture(
            Display.renderer,
            self._font.generate_surface(
                self._text,
                self._justify,
                self._width,
                int((self.gameobj.rotation if self.gameobj else 0) + self.rot_offset),
            )
        )

    def draw(self, camera: Camera):
        if self.hidden:
            return

        if self.gameobj.rotation != self._stored_rot:
            self._stored_rot = self.gameobj.rotation + self.rot_offset
            self.generate_surface()

        Draw.queue_texture(
            self._tx,
            camera.transform(self.gameobj.pos + (self._anchor - 1) * Vector(*self._tx.size) / 2) + self.offset,
            self.true_z
        )

    def delete(self):
        """Deletes the text component."""
        self._tx.destroy()
        self._font.close()
        self._tx = None
        self._font = None

    def clone(self) -> Text:
        """Clones the text component."""
        return Text(
            text=self._text,
            font=self._font,
            anchor=self._anchor,
            justify=self._justify,
            width=self._width,
            offset=self.offset,
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )
