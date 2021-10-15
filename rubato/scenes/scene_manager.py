from rubato import check_types
from rubato.scenes.scene import Scene


class SceneManager:
    """
    The Scene Manager houses a collection of scenes and allows switching between different scenes.
    Also handles the drawing and updating of current scene.
    """
    def __init__(self):
        self.scenes = {}
        self.min_id = 0
        self.current = 0

    def add(self, scene: Scene, scene_id: int | str = "") -> int | str:
        """
        Creates a new scene and adds it to the scene manager.

        :param scene: A scene object.
        :param scene_id: The id for the new scene. defaults to an incrementing value.
        :return: The scene's id value.
        """
        check_types(SceneManager.add, locals())
        if scene_id == "":
            scene_id = self.min_id
            self.min_id += 1

        if scene_id in self.scenes.keys():
            raise ValueError(f"The scene id {scene_id} is not unique in this manager")

        self.scenes[scene_id] = scene
        return scene_id

    @property
    def is_empty(self) -> bool:
        """
        Property method to check if the scene is empty.

        :return: Returns whether the scene list is empty.
        """
        check_types(SceneManager.is_empty, locals())
        return not bool(self.scenes.keys())

    def set(self, scene_id: int or str):
        """
        Changes the current scene to a new scene.

        :param scene_id: The id of the new scene.
        """
        check_types(SceneManager.set, locals())
        self.current = scene_id

    @property
    def current_scene(self) -> Scene:
        """
        Get the Scene class of the current scene.

        :return: The Scene class of the current scene.
        """
        check_types(SceneManager.current_scene, locals())
        return self.scenes.get(self.current)

    def update(self):
        """
        Calls the update function of the current scene.
        """
        check_types(SceneManager.update, locals())
        if self.is_empty: return
        self.current_scene.update()

    def draw(self):
        """
        Calls the draw function of the current scene.
        """
        check_types(SceneManager.draw, locals())
        if self.is_empty: return
        self.current_scene.draw()

