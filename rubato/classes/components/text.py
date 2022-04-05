"""A text component."""
from __future__ import annotations
import sdl2, sdl2.sdlttf, sdl2.ext

from . import Component
from ... import Defaults, Display, Vector, Color


class Text(Component):
    """A text component subclass. Add this to game objects or UI elements to give them text."""

    def __init__(self, options: dict = {}):
        """
        Initializes a Label.

        Args:
            options: A Text config. Defaults to the :ref:`Text defaults <textdef>`.
        """
        param = Defaults.text_defaults | options
        super().__init__()
        self._text = param["text"]
        self._font = param["font"]
        self._align = param["align"]
        self._justify = param["justify"]
        self._width = param["width"]

        self.generate_surface()

    @property
    def text(self) -> str:
        """The text of the Text."""
        return self._text

    @text.setter
    def text(self, text: str):
        """
        Sets the text of the Text.

        Args:
            text: The text to set.
        """
        self._text = text
        self.generate_surface()

    @property
    def justify(self) -> str:
        """The justification of the text."""
        return self._justify

    @justify.setter
    def justify(self, new: str):
        if new in ["left", "center", "right"]:
            self._justify = new
            self.generate_surface()
        else:
            raise ValueError(f"Justification {new} is not left, center or right.")

    @property
    def align(self) -> str:
        """The alignment vector of the text."""
        return self._align

    @align.setter
    def align(self, new: Vector):
        self._align = new

    @property
    def width(self) -> int:
        """The maximum width of the text. Will automatically wrap the text."""
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width
        self.generate_surface()

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
            Display.renderer, self._font.generate_surface(self._text, self._justify, self._width)
        )

    def draw(self):
        Display.update(
            self._tx, self.gameobj.map_coord(self.gameobj.pos + (self._align - 1) * Vector(*self._tx.size) / 2)
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
                "align": self._align,
                "justify": self._justify,
                "width": self._width,
            }
        )
