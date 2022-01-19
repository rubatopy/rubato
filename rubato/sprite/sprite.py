from rubato.utils import Display, Vector
from pygame.transform import scale
from pygame.surface import Surface
from rubato.scenes import Camera

class Sprite:
    """
    The base sprite class.

    :param options: A sprite :ref:`config <defaultsprite>`
    """

    default_options = {
        "pos": Vector(),
        "z_index": 0
    }

    def __init__(self, options: dict = {}):
        self.param = Sprite.merge_params(options, Sprite.default_options)
        self.pos = self.param["pos"]
        self.state = {}
        self.z_index = self.param["z_index"]
        self.in_frame = False

    def update(self):
        """The update loop"""
        pass

    def draw(self, surface: Surface, camera: Camera):
        """
        A generalized draw functions for any surface

        :param surface: The surface to draw the sprite on.
        :param camera: The camera to render the sprites with.
        """
        width, height = surface.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        Display.update(scale(surface, new_size), camera.transform(Sprite.center_to_tl(self.pos, Vector(width, height)) * camera.zoom))

    @staticmethod
    def center_to_tl(center: Vector, dims: Vector) -> Vector:
        """
        Converts center coordinates to top left coordinates

        :param center: The top left coordinate as a Vector
        :param dims: The width and the height of the item as a sprite as a Vector
        """
        return (center - (dims/2)).ceil()

    @staticmethod
    def merge_params(options: dict, defaults: dict) -> dict:
        """
        Merges an incomplete options dictionary with the defaults dictionary

        :param options: The incomplete options dictionary
        :param defaults: The default dictionary
        :return: The merged dictionary
        """
        merged = {}
        keys = defaults.keys()

        for key in keys:
            merged[key] = options.get(key, defaults[key])

        return merged


    def is_in_frame(self, camera: Camera, game) -> bool:
        draw_area_tl = (camera.pos - game.window_size).ceil()
        draw_area_br = (camera.pos + game.window_size).ceil()
        try:
            sprite_tl = (self.pos - Vector(self.image.image.get_width(), self.image.image.get_height())).ceil()
            sprite_br = (self.pos + Vector(self.image.image.get_width(), self.image.image.get_height())).ceil()
        except AttributeError:
            sprite_tl = (self.pos - Vector(self.image.get_width(), self.image.get_height())).ceil()
            sprite_br = (self.pos + Vector(self.image.get_width(), self.image.get_height())).ceil()

        return not (sprite_tl.x > draw_area_br.x or sprite_br.x < draw_area_tl.x or sprite_tl.y > draw_area_br.y or sprite_br.y < draw_area_tl.y)
