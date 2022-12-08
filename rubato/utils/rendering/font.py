"""A font abstraction used to render text."""
from typing import Literal
import sdl2, sdl2.sdlttf, sdl2.ext
from importlib.resources import files
import ctypes

from .. import Color


class Font:
    """
    This is the font object that is used to render text.

    Args:
        font: The font to use. Can also be a path to a font file. Defaults to Roboto.
            Included fonts are "Comfortaa", "Fredoka", "Merriweather", "Roboto", "SourceCodePro", "Mozart"
        size: The size of the font in pixels. Defaults to 16.
        styles: The styles to apply to the font. Set multiple styles by adding them together. Defaults to 0.
            These are the values you can use: Font.BOLD, Font.ITALIC, Font.UNDERLINE, Font.STRIKETHROUGH.
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

    BOLD = sdl2.sdlttf.TTF_STYLE_BOLD
    ITALIC = sdl2.sdlttf.TTF_STYLE_ITALIC
    UNDERLINE = sdl2.sdlttf.TTF_STYLE_UNDERLINE
    STRIKETHROUGH = sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH

    def __init__(
        self,
        font: str | Literal["Comfortaa", "Fredoka", "Merriweather", "Roboto", "SourceCodePro", "Mozart"] = "Roboto",
        size: int = 16,
        styles: int = 0,
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
        self.apply_styles()

    def _generate(self, text: str, align: str, width: int | float = 0) -> sdl2.SDL_Surface:
        """
        Generate a surface containing the text.

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

    def add_style(self, *styles: int):
        """
        Adds a style to the font.
        Style can be one of the following: Font.BOLD, Font.ITALIC, Font.UNDERLINE, Font.STRIKETHROUGH.


        Args:
            style: The style to add. You can add multiple styles. Or | them together.
        """
        # For developer: now that style is an bit map, 0000, each bit represents a style
        for style in styles:
            if 0 <= style <= 15:
                self._styles |= style
                self.apply_styles()
            else:
                raise ValueError("Style is not valid.")

    def remove_style(self, *styles: int):
        """
        Removes a style from the font.
        Style can be one of the following: Font.BOLD, Font.ITALIC, Font.UNDERLINE, Font.STRIKETHROUGH.

        Args:
            style: The style to remove. You can add multiple styles. Or | them together.
        """
        for style in styles:
            if 0 <= style <= 15:
                self._styles &= ~style
                self.apply_styles()
            else:
                raise ValueError("Style is not valid.")

    def apply_styles(self):
        """Applies the styles to the font."""
        sdl2.sdlttf.TTF_SetFontStyle(self._font.get_ttf_font(), self._styles)

    def clone(self):
        """
        Clones the font.
        """
        return Font(self._font_path, self._size, self._styles, self._color.clone())

    def __del__(self):
        self._font.close()
