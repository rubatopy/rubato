"""The font module for text rendering"""
import os
import sdl2, sdl2.sdlttf, sdl2.ext

from . import Defaults, Color


class Font:
    """
    This is the font object that is used to render text.
    """

    def __init__(self, options: dict = {}):
        param = Defaults.font_defaults | options
        self._size = param["size"]
        self._styles = param["styles"]
        self._color = param["color"] if isinstance(param["color"], Color) else Color(*param["color"])

        if param["font"] in Defaults.text_fonts:
            self._font = os.path.abspath(
                os.path.join(os.path.abspath(__file__), "../../" + Defaults.text_fonts[param["font"]])
            )
        else:
            self._font = param["font"]

        try:
            self._tx = sdl2.ext.FontTTF(self._font, self._size, self._color.to_tuple())
        except ValueError as e:
            raise FileNotFoundError("Font " + param["font"] + " cannot be found.") from e

        self.apply_styles()

    def generate_surface(
        self, text: str, align: str = Defaults.text_defaults["align"], width: int = Defaults.text_defaults["width"]
    ):
        try:
            return self._tx.render_text(text, width=None if width < 0 else width, align=align)
        except RuntimeError as e:
            raise ValueError(f"The width {width} is too small for the text.") from e
        except OSError as e:
            raise ValueError(f"The size {self._size} is too big for the text.") from e

    @property
    def size(self) -> int:
        """The size of the text in points."""
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size
        sdl2.sdlttf.TTF_SetFontSize(self._tx, size)

    @property
    def color(self) -> Color:
        """The color of the text."""
        return self._color

    @color.setter
    def color(self, color: Color):
        """
        Sets the color of the text.

        Args:
            color: The color to set.
        """
        self._color = color
        self._tx = sdl2.ext.FontTTF(self._font, self._size, self._color.to_tuple())

    def add_style(self, style: str):
        """
        Adds a style to the font.

        Args:
            style: The style to add. Can be one of the following: bold, italic, underline, strikethrough.
        """
        if style in Defaults.text_styles and style not in self._styles:
            self._styles.append(style)
            self.apply_styles()
        else:
            raise ValueError(f"Style {style} is not valid or is already applied.")

    def remove_style(self, style: str):
        """
        Removes a style from the font.

        Args:
            style: The style to remove. Can be one of the following: bold, italic, underline, strikethrough.
        """
        if style in self._styles:
            self._styles.remove(style)
            self.apply_styles()
        else:
            raise ValueError(f"Style {style} is not currently applied.")

    def apply_styles(self):
        """Applies the styles to the font."""
        s = Defaults.text_styles["normal"]
        for style in self._styles:
            s |= Defaults.text_styles[style]

        sdl2.sdlttf.TTF_SetFontStyle(self._tx.get_ttf_font(), s)
