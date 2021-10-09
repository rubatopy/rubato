from pgp.sprite.sprite import Sprite
from pgp.utils import Point

class RigidBody(Sprite):
    def __init__(self, pos: Point = Point()):
        super().__init__(pos)

    def physics(self):
        # TODO: Do the physics here
        pass

    def update(self):
        self.physics()

    def draw(self, camera):
        pass
