"""A text component."""
import os
import sdl2, sdl2.sdlttf, sdl2.ext

from . import Component
from ... import Defaults, Color, Display, Game, Vector


class Text(Component):
    """A text class"""

    fonts = {
        "Comfortaa": "../../../static/fonts/Comfortaa-Regular.ttf",
        "Fredoka": "../../../static/fonts/Fredoka-Regular.ttf",
        "Merriweather": "../../../static/fonts/Merriweather-Regular.ttf",
        "Roboto": "../../../static/fonts/Roboto-Regular.ttf",
        "SourceCodePro": "../../../static/fonts/SourceCodePro-Regular.ttf",
    }

    styles = {
        "bold": sdl2.sdlttf.TTF_STYLE_BOLD,
        "italic": sdl2.sdlttf.TTF_STYLE_ITALIC,
        "underline": sdl2.sdlttf.TTF_STYLE_UNDERLINE,
        "strikethrough": sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH,
        "normal": sdl2.sdlttf.TTF_STYLE_NORMAL,
    }

    def __init__(self, options: dict = {}):
        """
        Initializes an Text.

        Args:
            options: A Text config. Defaults to the |default| for
                    `Text`.
        """
        param = Defaults.text_defaults | options
        super().__init__()
        self._size = param["size"]
        self._style = param["style"]
        self._text = param["text"]
        self._color = Color(*param["color"]) if not isinstance(param["color"], Color) else param["color"]
        self._align = param["align"]
        self._width = param["width"]

        if param["font"] in Text.fonts:
            fontfile = os.path.abspath(os.path.join(os.path.abspath(__file__), Text.fonts[param["font"]]))
        else:
            fontfile = param["font"]

        try:
            self._font = sdl2.ext.FontTTF(fontfile, self._size, self._color.to_tuple())
        except ValueError as e:
            raise FileNotFoundError(f"Font {param['font']} cannot be found.") from e

        self.apply_style()
        self.generate_surface()

    @property
    def text(self) -> str:
        """The text of the text."""
        return self._text

    @text.setter
    def text(self, text: str):
        """
        Sets the text of the text.

        Args:
            text: The text to set.
        """
        self._text = text
        self.generate_surface()

    @property
    def size(self) -> int:
        """The size of the text."""
        return self._size

    @size.setter
    def size(self, size: int):
        self._size = size
        sdl2.sdlttf.TTF_SetFontSize(self._font, self._size)

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
        self.generate_surface()

    @property
    def align(self) -> str:
        """The alignment of the text."""
        return self._align

    @align.setter
    def align(self, new: str):
        if new in ["left", "center", "right"]:
            self._align = new
            self.generate_surface()
        else:
            raise ValueError(f"Alignment {new} is not left, center or right.")

    @property
    def width(self) -> int:
        """The maximum width of the text. Will automatically wrap the text."""
        return self._width

    @width.setter
    def width(self, width: int):
        self._width = width
        self.generate_surface()

    def add_style(self, style: str):
        """
        Adds a style to the text.

        Args:
            style: The style to add. Can be one of the following: bold, italic, underline, strikethrough.
        """
        if style in Text.styles and style not in self._style:
            self._style.append(style)
            self.apply_style()
        else:
            raise ValueError(f"Style {style} is not valid or is already applied.")

    def remove_style(self, style: str):
        """
        Removes a style from the text.

        Args:
            style: The style to remove. Can be one of the following: bold, italic, underline, strikethrough.
        """
        if style in self._style:
            self._style.remove(style)
            self.apply_style()
        else:
            raise ValueError(f"Style {style} is not currently applied.")

    def apply_style(self):
        """Applies the style to the text."""
        s = Text.styles["normal"]
        for style in self._style:
            s |= Text.styles[style]

        sdl2.sdlttf.TTF_SetFontStyle(self._font.get_ttf_font(), s)
        self.generate_surface()

    def generate_surface(self):
        """Generates the surface of the text."""
        try:
            self._surf = self._font.render_text(
                self._text, width=None if self.width < 0 else self.width, align=self._align
            )
        except RuntimeError as e:
            raise RuntimeError(f"The width {self.width} is too small for the text.") from e
        self._tx = sdl2.ext.Texture(Display.renderer, self._surf)

    def draw(self):
        """Draws the text."""
        if self.gameobj.z_index <= Game.camera.z_index:

            Display.update(self._tx, self.gameobj.map_coord(self.gameobj.pos - Vector(*self._tx.size) / 2))
