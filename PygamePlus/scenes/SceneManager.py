from Scene import Scene


class SceneManager:
    """
    A Scene Manager houses a collection of scenes and allows switching between different scenes.
    Also handles the drawing and updating of a scene.
    """
    def __init__(self):
        self.scenes = {}
        self.current = 0

    def new(self):
        """
        Creates a new scene and adds it to the scene manager
        """
        new_scene = Scene()  # TODO Make parameters
        self.scenes["id"] = new_scene  # TODO Actually set the ID

    def set(self, scene_id):
        """
        Changes the current scene to a new scene

        :param scene_id: The id of the new scene
        """
        self.current = scene_id

    def currentScene(self):
        """
        Get the Scene class of the current scene

        :return: The Scene class of the current scene
        """
        return self.scenes.get(self.current)

    def update(self):
        """
        Calls the update function of the current scene
        """
        pass  # TODO call update function of current scene

    def draw(self):
        """
        Calls the draw function of the current scene
        """
        pass  # TODO call the draw function of the current scene