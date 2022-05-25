"""The font module for text rendering"""
from typing import List, Literal
import sdl2, sdl2.sdlttf, sdl2.ext, sdl2.sdlgfx
from importlib.resources import files

from . import Color, Vector


class Font:
    """
    This is the font object that is used to render text.

    Args:
        font: The font to use. Can be one of the following: Comfortaa, Fredoka, Merriweather, Roboto, SourceCodePro,
            PressStart. Can also be a path to a font file. Defaults to Roboto.
        size: The size of the font. Defaults to 16.
        styles: The styles to apply to the font. Defaults to ["normal"].
        color: The color of the font. Defaults to Color(0, 0, 0).
    """

    text_fonts = {
        "Comfortaa": "Comfortaa-Regular.ttf",
        "Fredoka": "Fredoka-Regular.ttf",
        "Merriweather": "Merriweather-Regular.ttf",
        "Roboto": "Roboto-Regular.ttf",
        "SourceCodePro": "SourceCodePro-Regular.ttf",
        "PressStart": "PressStart2P-Regular.ttf",
    }

    text_styles = {
        "bold": sdl2.sdlttf.TTF_STYLE_BOLD,
        "italic": sdl2.sdlttf.TTF_STYLE_ITALIC,
        "underline": sdl2.sdlttf.TTF_STYLE_UNDERLINE,
        "strikethrough": sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH,
        "normal": sdl2.sdlttf.TTF_STYLE_NORMAL,
    }

    def __init__(
        self,
        font: str | Literal["Comfortaa", "Fredoka", "Merriweather", "Roboto", "SourceCodePro", "PressStart"] = "Roboto",
        size: int = 16,
        styles: List[Literal["normal", "bold", "italic", "underline", "strikethrough"]] = ["normal"],
        color: Color = Color(0, 0, 0),
    ):
        self._size = size
        self._styles = styles
        self._color = color

        if font in Font.text_fonts:
            self._font_path = str(files("rubato.static.fonts").joinpath(Font.text_fonts[font]))
        else:
            self._font_path = font

        try:
            self._font = sdl2.ext.FontTTF(self._font_path, self._size, self._color.to_tuple())
        except ValueError as e:
            raise FileNotFoundError(f"Font {font} cannot be found.") from e

        self.apply_styles()

    @property
    def size(self) -> int:
        """The size of the text in points."""
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size
        sdl2.sdlttf.TTF_SetFontSize(self._font, size)

    @property
    def color(self) -> Color:
        """The color of the text."""
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color
        self._font = sdl2.ext.FontTTF(self._font_path, self._size, self._color.to_tuple())

    def generate_surface(self, text: str, align: str = Vector(0, 0), width: int = 0, rot: int = 0) -> sdl2.SDL_Surface:
        """
        Generate the surface containing the text.

        Args:
            text: The text to render.
            align: The alignment to use. Defaults to Vector(0, 0).
            width: The maximum width to use. Defaults to -1.
            rot: The rotation of the text in degrees. Defaults to 0.

        Raises:
            ValueError: The width is too small for the text.
            ValueError: The size of the text is too large for the font.

        Returns:
            sdl2.SDL_Surface: The surface containing the text.
        """
        try:

            return sdl2.sdlgfx.rotozoomSurface(
                self._font.render_text(text, width=None if width < 0 else width, align=align), rot, 1, 1
            )
        except RuntimeError as e:
            raise ValueError(f"The width {width} is too small for the text.") from e
        except OSError as e:
            raise ValueError(f"The size {self._size} is too big for the text.") from e

    def add_style(self, style: str):
        """
        Adds a style to the font.

        Args:
            style: The style to add. Can be one of the following: bold, italic, underline, strikethrough.
        """
        if style in Font.text_styles and style not in self._styles:
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
        s = Font.text_styles["normal"]
        for style in self._styles:
            s |= Font.text_styles[style]

        sdl2.sdlttf.TTF_SetFontStyle(self._font.get_ttf_font(), s)
