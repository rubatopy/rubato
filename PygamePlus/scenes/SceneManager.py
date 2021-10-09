from PygamePlus.scenes.Scene import Scene


class SceneManager:
    """
    A Scene Manager houses a collection of scenes and allows switching between different scenes.
    Also handles the drawing and updating of current scene.
    """
    def __init__(self):
        self.scenes = {}
        self.current = 0

    def new(self, scene_id):
        """
        Creates a new scene and adds it to the scene manager

        :param scene_id: the id for the new scene
        :return: the newly created scene class
        """
        if scene_id in self.scenes.keys():
            raise ValueError(f"The id {scene_id} is not unique in this scene manager. Scene id's must be unique")
        else:
            new_scene = Scene(scene_id)
            self.scenes[scene_id] = new_scene
            return new_scene

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
        self.currentScene().update()

    def draw(self):
        """
        Calls the draw function of the current scene
        """
        self.currentScene().draw()

