from rubato.utils import Display, Vector, check_types
from pygame.transform import scale
from pygame.surface import Surface
from rubato.scenes import Camera
import math


class Sprite:
    """
    The base sprite class.

    :param pos: The position of the sprite on screen. Defaults to (0, 0, 0)
    """

    def __init__(self, pos: Vector = Vector()):
        check_types(Sprite.__init__, locals())
        self.pos = pos
        self.state = {}

    def update(self):
        """The update loop"""
        check_types(Sprite.update, locals())
        pass

    def draw(self, surface: Surface, camera: Camera):
        """
        A generalized draw functions for any surface

        :param surface: The surface to draw the sprite on.
        :param camera: The camera to render the sprites with.
        """
        check_types(Sprite.draw, locals())
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
        check_types(Sprite.center_to_tl, locals())
        return (center - (dims/2)).ceil()
