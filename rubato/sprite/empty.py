from rubato.sprite import Sprite
from rubato.scenes import Camera


class Empty(Sprite):
    def __init__(self):
        super().__init__()

    def update(self):
        pass

    def draw(self):
        pass

    def is_in_frame(self, camera: Camera, game):
        pass
