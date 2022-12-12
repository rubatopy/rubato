"""
A simple tilemap doesn't need to use the Tiled editor. It uses an array of
numbers to keep track of tile types.
"""
from __future__ import annotations
from .. import Component, Rectangle
from .... import Vector, Surface, Draw
from copy import deepcopy


class SimpleTilemap(Component):
    """
    A simple tilemap doesn't need to use the Tiled editor. It uses an array of numbers to keep track of tile types.

    Args:
        tilemap: A 2D array of integers representing the tilemap.
        tiles: A list of surfaces representing the tiles. The index of the surface in the list is the number used in the
            tilemap array.
        tile_size: The size of each tile in the tilemap.
        collision: A list of integers representing the tiles that should have collision.
        collider_tag: A list of strings representing the tags of the colliders. The index of the tag in the list is the
            number used in the tilemap array.
        scale: The scale of the tilemap.
        offset: The offset of the tilemap.
        rot_offset: The rotation offset of the tilemap.
        z_index: The z-index of the tilemap.
        hidden: Whether the tilemap is hidden.
    """

    def __init__(
        self,
        tilemap: list[list[int]],
        tiles: list[Surface],
        tile_size: Vector | tuple[int, int] = (32, 32),
        collision: list[int] | None = None,
        collider_tag: list[str] | None = None,
        scale: Vector | tuple[float, float] = (1, 1),
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False
    ):
        super().__init__(offset, rot_offset, z_index, hidden)

        self._map = tilemap
        self._tiles = tiles
        self._tile_size = Vector.create(tile_size)
        self._collision = collision if collision is not None else []
        self._collider_tag = collider_tag if collider_tag is not None else []
        self.scale = Vector.create(scale)
        """The scale of the tilemap."""
        self._result = Surface(1, 1, scale)

        self.uptodate = False
        """Whether the tilemap is up to date."""

    def _regen(self):
        dims = max([len(row) for row in self._map]), len(self._map)
        self._result = Surface(int(dims[0] * self._tile_size.x), int(dims[1] * self._tile_size.y))

        for i, row in enumerate(self._map):
            y = (i * self._tile_size.y) - self._result.height / 2 + self._tile_size.y / 2
            for j, tile in enumerate(row):
                x = (j * self._tile_size.x) - self._result.width / 2 + self._tile_size.x / 2
                self._result.blit(self._tiles[tile], dst=(int(x), int(y)))
                if tile in self._collision:
                    self.gameobj.add( # TODO: add to a child gameobject when that's a thing
                        Rectangle(
                            *(self._tile_size * self.scale).tuple_int(),
                            tag=self._collider_tag[tile] if tile < len(self._collider_tag) else "",
                            offset=(x, y) * self.scale,
                        )
                    )

    def update(self):
        if not self.uptodate:
            self._regen()
            self.uptodate = True

    def draw(self, camera):
        self._result.scale = self.scale
        self._result.rotation = self.true_rotation()
        Draw.queue_surface(self._result, self.true_pos(), self.true_z(), camera)

    def clone(self) -> SimpleTilemap:
        s = SimpleTilemap(
            deepcopy(self._map),
            [surf.clone() for surf in self._tiles],
            self._tile_size.clone(),
            deepcopy(self._collision),
            deepcopy(self._collider_tag),
            self.scale.clone(),
            self.offset.clone(),
            self.rot_offset,
            self.z_index,
            self.hidden,
        )
        s._result = self._result.clone()
        return s
