from .. import Component, Spritesheet, Rectangle, Circle, Polygon
from .... import Vector, get_path, Surface, Color, Draw, Display
import pytiled_parser as parse
import pytiled_parser.tiled_object as parse_obj
from pathlib import Path


class Tilemap(Component):

    def __init__(
        self, map_path: str, scale: Vector | tuple[float, float] = (1, 1), z_index: int = 0, hidden: bool = False
    ):
        super().__init__((0, 0), 0, z_index, hidden)
        self._scale = scale
        self._rects = []
        m = parse.parse_map(Path(get_path(map_path)))

        self._tileset = m.tilesets[1]
        self._sprites = Spritesheet(
            str(self._tileset.image),
            (self._tileset.tile_width, self._tileset.tile_height),
        )

        self._out = Surface(
            int(m.map_size.width * self._tileset.tile_width),
            int(m.map_size.height * self._tileset.tile_height),
            scale,
        )
        if (bg := m.background_color) is not None:
            self._out.fill(Color(bg.red, bg.green, bg.blue, bg.alpha))

        for layer in m.layers:
            if isinstance(layer, parse.LayerGroup):
                self._process_layergroup(layer)
            elif isinstance(layer, parse.TileLayer):
                self._process_tilelayer(layer)
            elif isinstance(layer, parse.ObjectLayer):
                self._process_objectlayer(layer)

    def _process_layergroup(self, layer: parse.LayerGroup, extra_offset: tuple = (0, 0)):
        if not layer.visible or layer.opacity == 0 or layer.layers is None:
            return

        for l in layer.layers:
            coords = (
                layer.coordinates.x + layer.offset.x + extra_offset[0],
                layer.coordinates.y + layer.offset.y + extra_offset[1],
            )

            if isinstance(l, parse.TileLayer):
                self._process_tilelayer(l, coords)
            elif isinstance(l, parse.ObjectLayer):
                self._process_objectlayer(l, coords)
            elif isinstance(l, parse.LayerGroup):
                self._process_layergroup(l, coords)

    def _process_tilelayer(self, layer: parse.TileLayer, extra_offset: tuple = (0, 0)):
        if layer.data is None or not layer.visible or layer.opacity == 0:
            return

        horiz_flip = 1 << 31
        vert_flip = 1 << 30
        diag_flip = 1 << 29

        l = Surface(self._out.width, self._out.height, (3, 3))

        for y, row in enumerate(layer.data):
            for x, tile in enumerate(row):
                if tile == 0:
                    continue

                flip_x, flip_y, flip_diag = False, False, False
                if tile & horiz_flip == horiz_flip:
                    flip_x = True
                    tile &= ~horiz_flip
                if tile & vert_flip == vert_flip:
                    flip_y = True
                    tile &= ~vert_flip
                if tile & diag_flip == diag_flip:
                    flip_diag = True
                    tile &= ~diag_flip

                t = self._sprites.get(
                    int((tile - 1) % self._sprites.grid_size.x),
                    int((tile - 1) // self._sprites.grid_size.x),
                ).clone()
                if flip_diag:
                    t.flip_anti_diagonal()
                if flip_x:
                    t.flip_x()
                if flip_y:
                    t.flip_y()

                if self._tileset.tiles and (t_info := self._tileset.tiles.get(tile - 1)) is not None:
                    if t_info.objects is not None and isinstance(t_info.objects, parse.ObjectLayer):
                        self._process_objectlayer(
                            t_info.objects, (x * self._tileset.tile_width, y * self._tileset.tile_height)
                        )

                l._blit(
                    t,
                    dst_rect=(
                        x * self._tileset.tile_width,
                        y * self._tileset.tile_height,
                        self._tileset.tile_width,
                        self._tileset.tile_height,
                    )
                )

        self._out._blit(
            l,
            dst_rect=(
                int(layer.coordinates.x + layer.offset.x + extra_offset[0]),
                int(layer.coordinates.y + layer.offset.y + extra_offset[1]),
                self._out.width,
                self._out.height,
            )
        )

    def _process_objectlayer(self, layer: parse.ObjectLayer, extra_offset: tuple = (0, 0)):
        if not layer.visible or layer.opacity == 0:
            return

        for obj in layer.tiled_objects:
            if not obj.visible:
                continue
            if isinstance(obj, parse_obj.Rectangle):
                p = (
                    extra_offset[0] + obj.coordinates.x + layer.offset.x + layer.coordinates.x,
                    extra_offset[1] + obj.coordinates.y + layer.offset.y + layer.coordinates.y,
                )
                p = Display._top_left_to_center(p, (obj.size.width, obj.size.height))
                p = self._out._convert_to_cartesian_space(p)
                p = (p[0] * self._scale[0], p[1] * self._scale[1])
                self._rects.append(
                    Rectangle(
                        round(obj.size.width * self._scale[0]),
                        round(obj.size.height * self._scale[1]),
                        offset=p,
                    )
                )
            elif isinstance(obj, parse_obj.Polygon):
                print(obj)
                p = (
                    extra_offset[0] + obj.coordinates.x + layer.offset.x + layer.coordinates.x,
                    extra_offset[1] + obj.coordinates.y + layer.offset.y + layer.coordinates.y,
                )
                p = Display._top_left_to_center(p, (obj.size.width, obj.size.height))
                p = self._out._convert_to_cartesian_space(p)
                p = (p[0] * self._scale[0], p[1] * self._scale[1])
                self._rects.append(
                    Polygon([(
                        x * self._scale[0],
                        -y * self._scale[1],
                    ) for x, y in obj.points], offset=p),
                )

    def setup(self):
        self.gameobj.add(*self._rects)

    def draw(self, camera):
        Draw.queue_surface(self._out, self.true_pos(), self.true_z(), camera)
