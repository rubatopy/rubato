from rubato.sprite import Image
from rubato.utils import Vector
from pygame.surface import Surface
from pygame.draw import rect

class Rectangle(Image):
    def __init__(self, center: Vector, dims: Vector, color: tuple, z_index: int = 0):
        super().__init__("empty", center, z_index=z_index)
        self.image = Surface(dims.to_tuple())

        rect(self.image, color, [0, 0, *dims.to_tuple()])