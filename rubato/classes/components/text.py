"""
A sprite used to render text.
"""
import pygame
from pygame.transform import scale
from rubato.classes.sprite import Sprite
from rubato.utils import Vector, Configs, Display
from rubato.classes import Camera
from rubato.utils.color import Color


class Text(Sprite):
    """
    A subclass of Sprite that handles Text.

    Attributes:
        text (str): The text to render.
        size (int): The font size of the text.
        font_name (str): The name of the font.
        color (Color): The color of the text
        static (bool): Whether or not the text should be unloaded.
        onto_surface (Union[pygame.Surface, None]): The surface to draw the
            text onto.
        image (pygame.Surface): The rendered text.
    """

    def __init__(self, options={}):
        """
        Initializes a text class.

        Args:
            options: A text config. Defaults to the |default| for `Text`.

        Raises:
            Exception: The font provided is not supported on the system.
        """
        param = Configs.merge_params(options, Configs.text_defaults)
        super().__init__({"pos": param["pos"], "z_index": param["z_index"]})
        self.text: str = param["text"]
        self.size: int = param["size"]
        self.font_name: str = param["font_name"]
        self.color: Color = param["color"]
        self.static: bool = param["static"]
        self.onto_surface: bool = param["onto_surface"]

        if self.onto_surface:
            self.draw = self.draw_onto_surface
        try:
            font = pygame.font.SysFont(self.font_name, self.size)
        except pygame.error:
            raise Exception(
                f"The font {self.font_name} is not supported on your system"
            ) from pygame.error
        self.image = font.render(self.text, True, self.color.to_tuple())

    def remake_image(self):
        """
        Rerender the text (after updating the text string for example).
        """
        font = pygame.font.SysFont(self.font_name, self.size)
        self.image = font.render(self.text, True, self.color)

    def draw(self, camera: Camera):  # pylint: disable=method-hidden
        """
        Draws the text if the z index is below the camera's.

        Args:
            camera: The current Camera viewing the scene.
        """
        width, height = self.image.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        Display.update(
            scale(self.image, new_size),
            camera.transform(
                Sprite.center_to_tl(camera.pos + self.pos, Vector(
                    width, height)) * camera.zoom),
        )

    def draw_onto_surface(self, camera: Camera):
        """
        Draws the text onto a surface.

        Args:
            camera: The current Camera viewing the scene.
        """
        width, height = self.image.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        self.onto_surface.blit(
            scale(self.image, new_size),
            (Sprite.center_to_tl(self.pos, Vector(width, height)) *
             camera.zoom).to_tuple(),
        )

    def is_in_frame(self, camera: Camera, game) -> bool:
        if self.static:
            return True
        return super().is_in_frame(camera, game)
