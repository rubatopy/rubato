from PygamePlus.Sprite import Sprite


class Group:
    """
    A group of sprites. Can render and update all of them at once.
    """
    def __init__(self):
        self.sprites = []

    def add(self, sprite: Sprite):
        """
        Adds a sprite to the groups.

        :param sprite: A sprite class to add to the group.
        :return: The sprite that was added.
        """
        self.sprites.append(sprite)
        return sprite

    def update(self):
        """Updates all the sprites in the group."""
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        """Draws all the sprites in the group."""
        for sprite in self.sprites:
            sprite.draw()