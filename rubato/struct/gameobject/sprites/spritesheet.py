"""
Utility class for loading spritesheets.
"""
import sdl2
import os

from . import Animation
from ... import Sprite
from .... import Vector, get_path, Display


class Spritesheet:
    """
    A spritesheet from the filesystem.

    Args:
        rel_path: The relative path to the spritesheet.
        sprite_size: The size of each sprite in the spritesheet. Defaults to (32, 32).
        grid_size: The size of the grid of sprites in the spritesheet. Set to None to automatically determine the
            grid size. Defaults to None.

    Raises:
        IndexError: If user does not load the entire sheet.
    """

    def __init__(
        self,
        rel_path: str,
        sprite_size: Vector | tuple[float, float] = (32, 32),
        grid_size: Vector | tuple[float, float] | None = None
    ):
        self._sprite_size: tuple[int, int] = (int(sprite_size[0]), int(sprite_size[1]))
        self._sheet = Sprite(rel_path=rel_path)
        self._sprites: list[list[Sprite]] = []

        if not grid_size:
            self._grid: tuple[int, int] = (self._sheet.get_size() / self._sprite_size).tuple_int()
        else:
            self._grid: tuple[int, int] = (int(grid_size[0]), int(grid_size[1]))
            if Vector(*self._sprite_size) * self._grid != self._sheet.get_size():
                raise IndexError("Sprite and grid size do not match given spritesheet size.")

        for y in range(0, self._grid[1] * self._sprite_size[1], self._sprite_size[1]):
            self._sprites.append([])
            for x in range(0, self._grid[0] * self._sprite_size[0], self._sprite_size[0]):
                sub = sdl2.SDL_CreateRGBSurfaceWithFormat(
                    0, self._sprite_size[0], self._sprite_size[1], 32, Display.pixel_format
                )
                sdl2.SDL_BlitSurface(
                    self._sheet.surf,
                    sdl2.SDL_Rect(x, y, self._sprite_size[0], self._sprite_size[1]),
                    sub,
                    sdl2.SDL_Rect(0, 0, self._sprite_size[0], self._sprite_size[1]),
                )

                sprite: Sprite = Sprite("")
                sprite.surf = sub.contents

                self._sprites[y // self._sprite_size[1]].append(sprite)

    @property
    def grid_size(self) -> Vector:
        """The size of the spritesheet grid (readonly)."""
        return Vector(*self._grid)

    @property
    def sprite_size(self) -> Vector:
        """The size of each sprite (readonly)."""
        return Vector(*self._sprite_size)

    @property
    def sheet(self) -> Sprite:
        """The actual spritesheet sprite (readonly)."""
        return self._sheet

    @property
    def sprites(self) -> list[list[Sprite]]:
        """The list of all the sprites as sprites (readonly)."""
        return self._sprites

    @property
    def end(self):
        """
        The end indexes of the Spritesheet as a vector.

        Example:
            You can use :code:`spritesheet.get(*spritesheet.end)` to get the final Sprite
        """
        return self.grid_size - Vector.one()

    def get(self, x: int, y: int) -> Sprite:
        """
        Gets the Sprite at the corresponding grid coordinate of the spritesheet.

        Args:
            x: The x grid coordinate.
            y: The y grid coordinate.

        Raises:
            IndexError: One or both of the coordinates are out of range of the spritesheet's size.

        Returns:
            The Sprite at the corresponding coordinate.
        """
        if x >= self.grid_size.x or y >= self.grid_size.y:
            raise IndexError(f"The coordinates ({x}, {y}) are out of range of the spritesheet.")
        return self.sprites[y][x].clone()

    @staticmethod
    def from_folder(
        rel_path: str,
        sprite_size: Vector | tuple[float, float],
        default_state=None,
        recursive: bool = True
    ) -> Animation:
        """
        Creates an Animation from a folder of spritesheets.
        Directory must be comprised solely of spritesheets.
        Added alphabetically. Default is the first sheet loaded.

        Args:
            rel_path: The relative path to the folder you wish to import
            sprite_size: The size of a single sprite in your spritesheet, should be the same in all imported sheets.
            default_state: Sets the default state of the animation.
            recursive: Whether it will import an animation shallowly or recursively. Defaults to True.

        Returns:
            Animation: the animation loaded from the folder of spritesheets
        """
        anim = Animation()

        path = get_path(rel_path)

        if not recursive:
            _, _, files = next(os.walk(path))
            # walk to directory path and ignore name and subdirectories
            files.sort()
            for sprite_path in files:
                path_to_spritesheet = os.path.join(path, sprite_path)
                sprite_sheet = Spritesheet(
                    rel_path=path_to_spritesheet,
                    sprite_size=sprite_size,
                )
                anim.add_spritesheet(sprite_path.split(".")[0], sprite_sheet, to_coord=sprite_sheet.end)
        else:
            for _, _, files in os.walk(path):
                # walk to directory path and ignore name and subdirectories
                files.sort()
                for sprite_path in files:
                    path_to_spritesheet = os.path.join(path, sprite_path)
                    sprite_sheet = Spritesheet(
                        rel_path=path_to_spritesheet,
                        sprite_size=sprite_size,
                    )
                    anim.add_spritesheet(sprite_path.split(".")[0], sprite_sheet, to_coord=sprite_sheet.end)

        if default_state:
            anim.default_state = default_state
            anim.current_state = default_state
            anim.reset()
        return anim
