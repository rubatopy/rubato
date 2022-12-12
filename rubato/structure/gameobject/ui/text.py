"""A text component."""
from __future__ import annotations
from typing import Literal
import sdl2, sdl2.ext

from .. import Component
from .... import Vector, Font, Draw, Camera, Surface


class Text(Component):
    """
    A text component. Add this to game objects or UI elements to give them text. Takes a font object to render the text.

    Args:
        text: The text to display. Defaults to "".
        font: The font to use. Defaults to Font().
        justify: The justification of the text. Defaults to "left".
        anchor: The anchor of the text. The zero vector means it is centered. x component is whether to shift left,
            none, or right (-1, 0, 1). y component is whether to shift top, none, or bottom (-1, 0, 1).
            Defaults to Vector(0, 0).
        width: The width of the text. Defaults to 0.
        af: Whether to use anisotropic filtering. Defaults to True.
        offset: The offset of the text from the game object. Defaults to Vector(0, 0).
        rot_offset: The rotation offset of the text from the game object. Defaults to 0.
        z_index: The z index of the text. Defaults to 0.
        hidden: Whether the text is hidden. Defaults to False.
    """

    def __init__(
        self,
        text: str = "",
        font: Font = Font(),
        justify: Literal["left", "center", "right"] = "left",
        anchor: Vector | tuple[float, float] = (0, 0),
        width: int = 0,
        af: bool = True,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index, hidden=hidden)
        self._text: str = text
        self.font_object: Font = font
        self.anchor: Vector = Vector.create(anchor)
        """
        The anchor vector of the text.

        This controls the position of the text relative to the game object. Is a vector where the x value
        controls the x anchor and the y value controls the y anchor. The values for each can be either -1, 0 or 1. This
        offset the text around the game object center.

        Example:
            An anchor of ``Vector(0, 0)`` will center the text on the game object. An anchor of ``Vector(1, 1)`` will
            move the text so that it's top left corner is at the game object's center.
        """
        self._justify: Literal["left", "center", "right"] = justify
        self._width: int = width
        self._af = af

        if not self.font_object:
            self.font_object = Font()

        self._uptodate = False

        self._font = self.font_object._font
        self._size = self.font_object._size
        self._color = self.font_object._color.clone()
        self._styles = self.font_object._styles

    @property
    def af(self) -> bool:
        """Whether to use anisotropic filtering."""
        return self._af

    @af.setter
    def af(self, new: bool):
        self._af = new
        self._uptodate = False

    @property
    def text(self) -> str:
        """The text of the Text."""
        return self._text

    @text.setter
    def text(self, new: str):
        self._text = new
        self._uptodate = False

    @property
    def justify(self) -> Literal["left", "center", "right"]:
        """
        The justification of the text.

        Can be one of: ``"left"``, ``"center"``, ``"right"``.
        """
        return self._justify

    @justify.setter
    def justify(self, new: Literal["left", "center", "right"]):
        if new not in ["left", "center", "right"]:
            raise ValueError(f"Justification {new} is not left, center or right.")
        self._justify = new
        self._uptodate = False

    @property
    def width(self) -> int:
        """The maximum width of the text. Will automatically wrap the text. Use -1 to disable wrapping."""
        return self._width

    @width.setter
    def width(self, new: int):
        self._width = new
        self._uptodate = False

    def _regen(self):
        """(Re)generates the surface of the text."""
        surf = self.font_object._generate(
            self._text,
            self._justify,
            self._width,
        )
        self._surf = Surface._from_surf(surf, af=self._af)
        sdl2.SDL_FreeSurface(surf)

    def update(self):
        # For developer: We need to check if the font object has changed compared to what we are rendering,
        # but a font object can be shared between different texts.
        if self._font != self.font_object._font or self._size != self.font_object._size or \
                self._color != self.font_object._color or self._styles != self.font_object._styles:
            self._font = self.font_object._font
            self._size = self.font_object._size
            self._color = self.font_object._color
            self._styles = self.font_object._styles
            self._uptodate = False
        if not self._uptodate:
            self._regen()
            self._uptodate = True

    def draw(self, camera: Camera):
        self._surf.rotation = self.true_rotation()
        Draw.queue_surface(
            self._surf,
            self.true_pos() + self.anchor * self._surf.size_scaled() / 2,
            self.true_z(),
            camera,
        )

    def clone(self) -> Text:
        """Clones the text component."""
        return Text(
            text=self._text,
            font=self.font_object.clone(),
            anchor=self.anchor.clone(),
            justify=self._justify,
            width=self._width,
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )
