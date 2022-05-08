"""A text component."""
from __future__ import annotations
from typing import TYPE_CHECKING
import sdl2, sdl2.sdlttf, sdl2.ext

from . import Component
from ... import Defaults, Display, Vector, Color, Font

if TYPE_CHECKING:
    from .. import Camera


class Text(Component):
    """
    A text component subclass. Add this to game objects or UI elements to give them text.

    Args:
        options: A Text config. Defaults to the :ref:`Text defaults <textdef>`.
    """

    def __init__(self, options: dict = {}):
        params = Defaults.text_defaults | options
        super().__init__(params)
        self._text: str = params["text"]
        self._font: Font = params["font"]
        self._anchor: str = params["anchor"]
        self._justify: str = params["justify"]
        self._width: int = params["width"]
        self._stored_rot: int = 0

        if not self._font:
            self._font = Font()

        self.generate_surface()

    @property
    def text(self) -> str:
        """The text of the Text."""
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text
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
    def width(self, width: int):
        self._width = width
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
                (self.gameobj.rotation if self.gameobj else 0) + self.rotation_offset,
            )
        )

    def draw(self, camera: Camera):
        if self.gameobj.rotation != self._stored_rot:
            self._stored_rot = self.gameobj.rotation + self.rotation_offset
            self.generate_surface()

        Display.update(
            self._tx,
            camera.transform(self.gameobj.pos + (self._anchor - 1) * Vector(*self._tx.size) / 2) + self.offset
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
            {
                "text": self._text,
                "font": self._font,
                "anchor": self._anchor,
                "justify": self._justify,
                "width": self._width,
            }
        )
