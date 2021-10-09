from PygamePlus.scenes.Scene import Scene


class SceneManager:
    """
    The Scene Manager houses a collection of scenes and allows switching between different scenes.
    Also handles the drawing and updating of current scene.
    """
    def __init__(self):
        self.scenes = {}
        self.min_id = 0
        self.current = 0

    def add_scene(self, scene: Scene, scene_id=None):
        """
        Creates a new scene and adds it to the scene manager

        :param scene: a scene object
        :param scene_id: the id for the new scene. defaults to an incrementing value
        :return: the scene's id value
        """
        if scene_id is None:
            scene_id = self.min_id
            self.min_id += 1

        if scene_id in self.scenes.keys():
            raise ValueError(f"The id {scene_id} is not unique in this scene manager. Scene id's must be unique")

        self.scenes[scene_id] = scene
        return scene_id

    def set(self, scene_id):
        """
        Changes the current scene to a new scene

        :param scene_id: The id of the new scene
        """
        self.current = scene_id

    @property
    def current_scene(self):
        """
        Get the Scene class of the current scene

        :return: The Scene class of the current scene
        """
        return self.scenes.get(self.current)

    def update(self):
        """
        Calls the update function of the current scene
        """
        self.current_scene().update()

    def draw(self):
        """
        Calls the draw function of the current scene
        """
        self.current_scene().draw()

