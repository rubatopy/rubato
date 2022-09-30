"""A font abstraction used to render text."""
from typing import Literal
import sdl2, sdl2.sdlttf, sdl2.ext
from importlib.resources import files
import ctypes

from . import Color


class Font:
    """
    This is the font object that is used to render text.

    Args:
        font: The font to use. Can also be a path to a font file. Defaults to Roboto.
        size: The size of the font in pixels. Defaults to 16.
        styles: The styles to apply to the font. Defaults to [].
            Fill with only the following: bold, italic, underline, strikethrough.
        color: The color of the font. Defaults to Color(0, 0, 0).
    """

    _text_fonts = {
        "Comfortaa": "Comfortaa-Regular.ttf",
        "Fredoka": "Fredoka-Regular.ttf",
        "Merriweather": "Merriweather-Regular.ttf",
        "Roboto": "Roboto-Regular.ttf",
        "SourceCodePro": "SourceCodePro-Regular.ttf",
        "Mozart": "Mozart-Regular.ttf",
    }

    _text_styles = {
        "bold": sdl2.sdlttf.TTF_STYLE_BOLD,
        "italic": sdl2.sdlttf.TTF_STYLE_ITALIC,
        "underline": sdl2.sdlttf.TTF_STYLE_UNDERLINE,
        "strikethrough": sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH,
    }

    def __init__(
        self,
        font: str | Literal["Comfortaa", "Fredoka", "Merriweather", "Roboto", "SourceCodePro", "Mozart"] = "Roboto",
        size: int = 16,
        styles: list[str] = [],
        color: Color = Color(0, 0, 0),
    ):
        self._size = size
        self._styles = styles
        self._color = color

        if font in Font._text_fonts:
            self._font_path = str(files("rubato.static.fonts").joinpath(Font._text_fonts[font]))
        else:
            self._font_path = font

        try:
            self._font = sdl2.ext.FontTTF(self._font_path, str(self._size) + "px", self._color.to_tuple())
        except ValueError as e:
            raise FileNotFoundError(f"Font {font} cannot be found.") from e

        self.apply_styles()

    @property
    def size(self) -> int:
        """The size of the text in points."""
        return self._size

    @size.setter
    def size(self, new: int):
        self._size = new
        sdl2.sdlttf.TTF_SetFontSize(self._font.get_ttf_font(), new)

    @property
    def color(self) -> Color:
        """The color of the text."""
        return self._color

    @color.setter
    def color(self, new: Color):
        self._color = new
        self._font = sdl2.ext.FontTTF(self._font_path, self._size, self._color.to_tuple())

    def generate_surface(self, text: str, align: str, width: int | float = 0) -> sdl2.SDL_Surface:
        """
        Generate the surface containing the text.

        Args:
            text: The text to render.
            align: The alignment to use.
            width: The maximum width to use. Defaults to -1.
            rot: The rotation of the text in degrees. Defaults to 0.

        Raises:
            ValueError: The width is too small for the text.
            ValueError: The size of the text is too large for the font.

        Returns:
            The surface containing the text.
        """
        try:
            return self._font.render_text(text, width=None if width <= 0 else round(width), align=align)
        except RuntimeError as e:
            raise ValueError(f"The width {width} is too small for the text.") from e
        except OSError as e:
            raise ValueError(f"The size {self._size} is too big for the text.") from e

    def size_text(self, text: str) -> tuple[int, int]:
        """
        Calculated the dimensions of a string of text using a given font.

        Args:
            text: The string of text to calculate dimensions for.

        Returns:
            The dimensions of the string.
        """
        text_w, text_h = ctypes.c_int(0), ctypes.c_int(0)
        sdl2.sdlttf.TTF_SizeText(self._font.get_ttf_font(), text.encode(), ctypes.byref(text_w), ctypes.byref(text_h))
        return (text_w.value, text_h.value)

    def add_style(self, style: str):
        """
        Adds a style to the font.

        Args:
            style: The style to add. Can be one of the following: bold, italic, underline, strikethrough.
        """
        if style in Font._text_styles and style not in self._styles:
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
        s = 0x00
        for style in self._styles:
            s |= Font._text_styles[style]

        sdl2.sdlttf.TTF_SetFontStyle(self._font.get_ttf_font(), s)

    def clone(self):
        """
        Clones the font.
        """
        return Font(self._font_path, self._size, self._styles, self._color.clone())

    def __del__(self):
        self._font.close()
