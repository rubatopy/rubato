class Scene:
    """
    A scene is a collection of sprites. Interactions between sprites is handled here.
    """

    def __init__(self, scene_id):
        """
        :param scene_id: A unique ID for the scene
        """
        self.sprites = []
        self.id = id

    def update(self):
        """
        The update loop for this scene
        """

    def draw(self):
        """
        The draw loop for this scene
        """