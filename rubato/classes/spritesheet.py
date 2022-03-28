"""A class to load, manage, and interact with spritesheets."""
import sdl2
import sdl2.ext
from typing import List
from rubato.utils import Defaults
from rubato.classes.components import Image
from rubato.utils import Vector


class Spritesheet():
    """A spritesheet from the filesystem."""

    def __init__(self, options: dict = {}):
        """
        Initializes a Spritesheet.

        Args:
            options: A Spritesheet config. Defaults to the |default| for
                `Spritesheet`.

        Raises:
            IndexError: If user does not load the entire sheet.
        """
        params = Defaults.spritesheet_defaults | options

        self._grid: Vector = params["grid_size"]
        self._sprite_size: Vector = params["sprite_size"]
        self._sheet = Image({"rel_path": params["rel_path"]})
        self._sprites: List[List[Image]] = []

        if (self._sprite_size * self._grid) != self._sheet.get_size():
            raise IndexError("Your sprite size or grid size is incorrect, please check")

        for y in range(0, self._grid.y * self._sprite_size.y, self._sprite_size.y):
            self._sprites.append([])
            for x in range(0, self._grid.x * self._sprite_size.x, self._sprite_size.x):
                sub = sdl2.SDL_CreateRGBSurfaceWithFormat(
                    0, self._sprite_size.x, self._sprite_size.y, 64, sdl2.SDL_PIXELFORMAT_RGBA32
                )
                sdl2.SDL_BlitSurface(
                    self._sheet.image,
                    sdl2.SDL_Rect(x, y, self._sprite_size.x, self._sprite_size.y),
                    sub,
                    sdl2.SDL_Rect(0, 0, self._sprite_size.x, self._sprite_size.y),
                )

                sprite = Image()
                sprite.image = sub.contents
                self._sprites[y // self._sprite_size.y].append(sprite)

    @property
    def grid_size(self) -> Vector:
        """The size of the spritesheet grid."""
        return self._grid

    @property
    def sprite_size(self) -> Vector:
        """The size of each sprite."""
        return self._sprite_size

    @property
    def sheet(self) -> Image:
        """The actual spritesheet image."""
        return self._sheet

    @property
    def sprites(self) -> List[List[Image]]:
        """The list of all the sprites as images"""
        return self._sprites

    def get(self, x: int, y: int) -> Image:
        """
        Gets the Image at the coorsponding grid coordinate of the spritesheet.

        Args:
            x: The x grid coordinate.
            y: The y grid coordinate.

        Raises:
            IndexError: One or both of the coordinates are out of range of the spritesheet's size.

        Returns:
            Image: The image of the cooresponding sprite.
        """
        if x >= self.grid_size.x or y >= self.grid_size.y:
            raise IndexError(f"The coordinates ({x}, {y}) are out of range of the spritesheet.")
        return self.sprites[y][x].clone()

    @property
    def end(self):
        """The last coordinate you can use the get function on (end of the Spritesheet)"""
        return self.grid_size - Vector.one
