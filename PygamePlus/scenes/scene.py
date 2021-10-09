class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled here.
    """

    def __init__(self):
        self.sprites = []

    # TODO Sprite add and remove functions
    def update(self):
        """
        The update loop for this scene.
        """
        for sprite in self.sprites:
            sprite.update()

    def draw(self):
        """
        The draw loop for this scene.
        """
        for sprite in self.sprites:
            sprite.draw()