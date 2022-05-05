"""
A module to load, manage, and interact with spritesheets.
"""
import sdl2
import sdl2.ext
from typing import List
import os

from . import Image, Animation
from ... import Defaults, Vector, get_path


class Spritesheet:
    """
    A spritesheet from the filesystem.

    Args:
        options: A Spritesheet config. Defaults to the :ref:`Spritesheet defaults <spritesheetdef>`.

    Raises:
        IndexError: If user does not load the entire sheet.
    """

    def __init__(self, options: dict = {}):
        params = Defaults.spritesheet_defaults | options

        self._grid: Vector = params["grid_size"]
        self._sprite_size: Vector = params["sprite_size"]
        self._sheet = Image({"rel_path": params["rel_path"]})
        self._sprites: List[List[Image]] = []
        if not self._grid:
            self._grid = self._sheet.get_size() / self._sprite_size
            self._grid = self._grid.to_int()
        if (self._sprite_size * self._grid) != self._sheet.get_size():
            raise IndexError("Your sprite size or grid size is incorrect, please check")

        for y in range(0, self._grid.y * self._sprite_size.y, self._sprite_size.y):
            self._sprites.append([])
            for x in range(0, self._grid.x * self._sprite_size.x, self._sprite_size.x):
                sub = sdl2.SDL_CreateRGBSurfaceWithFormat(
                    0, self._sprite_size.x, self._sprite_size.y, 32, sdl2.SDL_PIXELFORMAT_RGBA8888
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
        """The size of the spritesheet grid (readonly)."""
        return self._grid

    @property
    def sprite_size(self) -> Vector:
        """The size of each sprite (readonly)."""
        return self._sprite_size

    @property
    def sheet(self) -> Image:
        """The actual spritesheet image (readonly)."""
        return self._sheet

    @property
    def sprites(self) -> List[List[Image]]:
        """The list of all the sprites as images (readonly)."""
        return self._sprites

    @property
    def end(self):
        """
        The end indexes of the Spritesheet as a vector.

        Example:
            You can use :code:`spritesheet.get(*spritesheet.end)` to get the final image
        """
        return self.grid_size - Vector.one

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

    @staticmethod
    def from_folder(rel_path: str, sprite_size: Vector, default_state=None) -> Animation:
        """
        Creates an Animation from a folder of spritesheets.
        Directory must be comprised solely of spritesheets.
        Added alphabetically. Default is the first sheet loaded.

        Args:
            rel_path: The relative path to the folder you wish to import
            sprite_size: The size of a single sprite in your spritesheet, should be the same in all imported sheets.
            default_state: Sets the default state of the animation.

        Returns:
            Animation: the animation loaded from the folder of spritesheets
        """
        anim = Animation()

        path = get_path(rel_path)

        for _, _, files in os.walk(path):
            # walk to directory path and ignore name and subdirectories
            files.sort()
            for sprite_path in files:
                path_to_spritesheet = os.path.join(path, sprite_path)
                try:
                    sprite_sheet = Spritesheet({
                        "rel_path": path_to_spritesheet,
                        "sprite_size": sprite_size,
                    })
                    anim.add_spritesheet(sprite_path.split(".")[0], sprite_sheet, to_coord=sprite_sheet.end)
                except TypeError:
                    continue
        if default_state:
            anim.default_state = default_state
            anim.current_state = default_state
            anim.reset()
        return anim
