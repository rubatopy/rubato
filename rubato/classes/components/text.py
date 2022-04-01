"""A text component."""
import os
import sdl2, sdl2.sdlttf

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

        if param["font"] in Text.fonts:
            fontfile = os.path.abspath(os.path.join(os.path.abspath(__file__),
                                                    Text.fonts[param["font"]])).encode("utf-8")
            print(fontfile)
        else:
            fontfile = os.path.join(os.path.abspath(os.getcwd()), param["font"]).encode("utf-8")

        try:
            self._font = sdl2.sdlttf.TTF_OpenFont(fontfile, self._size).contents
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

        sdl2.sdlttf.TTF_SetFontStyle(self._font, s)
        self.generate_surface()

    def generate_surface(self):
        """Generates the surface of the text."""
        self._surf = sdl2.sdlttf.TTF_RenderUTF8_Solid(
            self._font, self._text.encode("utf-8"), sdl2.SDL_Color(*self._color.to_tuple())
        ).contents
        self._tx = sdl2.ext.Texture(Display.renderer, self._surf)

    def draw(self):
        """Draws the text."""
        if self.gameobj.z_index <= Game.camera.z_index:

            Display.update(self._tx, self.gameobj.map_coord(self.gameobj.pos - Vector(*self._tx.size) / 2))
