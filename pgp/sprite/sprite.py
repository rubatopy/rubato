from pgp.utils import Display, Vector, check_types
from pygame.transform import scale
from pygame.surface import Surface
from pgp.scenes import Camera


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
        Display.update(scale(surface, new_size), camera.transform(self.pos * camera.zoom))
