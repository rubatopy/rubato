"""
The default sprite class.
"""
from pygame.transform import scale
from pygame.surface import Surface
from rubato.scenes.camera import Camera
from rubato.utils import Display, Vector, Configs


class Sprite:
    """
    The base sprite class.

    Warning:
        This class should not be instantiated. Instead, a class should inherit
        from this.

    Attributes:
        param (dict[str, any]): A dictionary with all of the parameters of the
            sprite.
        pos (Vector): The current position of the sprite.
        z_index (int): The z_index of the sprite.
        in_frame (bool): Whether or not the sprite is in the frame.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a sprite.

        Args:
            options: A sprite config. Defaults to the |default| for
                `Sprite`.
        """
        param = Configs.merge_params(options, Configs.sprite_defaults)
        self.pos = param["pos"]
        self.z_index = param["z_index"]
        self.in_frame = False

    def is_in_frame(self, camera: Camera, game) -> bool:
        """
        Checks if the sprite is in the frame.

        Args:
            camera: The camera to check with.
            game (Game): The game the sprite is in.

        Returns:
            bool: Whether or not the sprite is in the frame.
        """
        draw_area_tl = (camera.pos - game.window_size).ceil()
        draw_area_br = (camera.pos + game.window_size).ceil()
        try:
            sprite_tl = (self.pos -
                         Vector(self.image.image.get_width(),
                                self.image.image.get_height())).ceil()
            sprite_br = (self.pos +
                         Vector(self.image.image.get_width(),
                                self.image.image.get_height())).ceil()
        except AttributeError:
            sprite_tl = (self.pos - Vector(self.image.get_width(),
                                           self.image.get_height())).ceil()
            sprite_br = (self.pos + Vector(self.image.get_width(),
                                           self.image.get_height())).ceil()

        return not (sprite_tl.x > draw_area_br.x
                    or sprite_br.x < draw_area_tl.x
                    or sprite_tl.y > draw_area_br.y
                    or sprite_br.y < draw_area_tl.y)

    def update(self):
        """The update loop"""
        pass

    def draw(self, surface: Surface, camera: Camera):
        """
        A generalized draw function for any surface

        Args:
            surface: The surface to draw.
            camera: The camera to draw onto.
        """
        width, height = surface.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        Display.update(
            scale(surface, new_size),
            camera.transform(
                Sprite.center_to_tl(self.pos, Vector(width, height)) *
                camera.zoom))

    @staticmethod
    def center_to_tl(center: Vector, dims: Vector) -> Vector:
        """
        Converts center coordinates to top left coordinates

        Args:
            center: The top left coordinate as a Vector
            dims: The width and the height of the item as a sprite as a Vector

        Returns:
            Vector: The new coordinates.
        """
        return (center - (dims / 2)).ceil()
