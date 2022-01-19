from rubato.sprite import Sprite
from rubato.utils import Vector, Color, Display
from rubato.scenes import Camera
import pygame
from pygame.transform import scale

class Text(Sprite):
    """
    A subclass of Sprite that handles Text.

    :param options: A text :ref:`config <defaulttext>`
    """

    default_options = {
        "text": "default_text",
        "pos": Vector(),
        "size": 16,
        "z_index": 0,
        "font_name": 'Arial',
        "color": Color.black,
        "static": False,
        "onto_surface": None,
    }

    def __init__(self, options={}):
        self.params = Sprite.merge_params(options, Text.default_options)
        super().__init__({"pos": self.params["pos"], "z_index": self.params["z_index"]})
        self.text = self.params["text"]
        self.size = self.params["size"]
        self.font_name = self.params["font_name"]
        self.color = self.params["color"]
        self.static = self.params["static"]
        self.onto_surface = self.params["onto_surface"]

        if self.onto_surface:
            self.draw = self.draw_onto_surface
        try:
            font = pygame.font.SysFont(self.font_name, self.size)
        except pygame.error:
            raise Exception(f"The font {self.font_name} is not supported on your system")
        self.image = font.render(self.text, True, self.color)

    def remake_image(self):
        font = pygame.font.SysFont(self.font_name, self.size)
        self.image = font.render(self.text, True, self.color)

    def draw(self, camera: Camera):
        """
        Draws the text if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """
        width, height = self.image.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        Display.update(scale(self.image, new_size),
        camera.transform(Sprite.center_to_tl(camera.pos + self.pos, Vector(width, height)) * camera.zoom))

    def draw_onto_surface(self, camera: Camera):
        """
        Draws the text if the z index is below the camera's.

        :param camera: The current Camera viewing the scene.
        """
        width, height = self.image.get_size()
        new_size = (round(width * camera.zoom), round(height * camera.zoom))
        self.onto_surface.blit(scale(self.image, new_size),
                               (Sprite.center_to_tl(self.pos, Vector(width, height)) * camera.zoom).to_tuple())

    def is_in_frame(self, camera: Camera, game) -> bool:
        if self.static:
            return True
        return super().is_in_frame(camera, game)
