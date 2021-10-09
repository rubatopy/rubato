from pgp.sprite.sprite import Sprite
from pygame.image import load
from pgp.utils import GD, Point

class Image(Sprite):
    def __init__(self, image_location: str, pos: Point = Point()):
        self.image = load(image_location)
        super().__init__(pos)

    def update(self):
        pass

    def draw(self, camera):
        if camera.pos.z >= self.pos.z:
            GD.update(self.image, camera.transform(self.pos))
