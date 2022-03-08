"""
The Scene Manager houses a collection of scenes and allows switching between
different scenes. Each Game object has a scene manager. It also handles drawing
and updating the current scene.
"""
from typing import Union
from rubato.classes.scene import Scene
from rubato.utils.error import IdError


class SceneManager:
    """
    The Scene Manager contains and handle multiple scenes.

    Attributes:
        scenes (dict[Union[int, str], Scene]): The collection of scenes in the
            manager. Accessed by scene id.
        current (Union[int, str]): The id of the current scene.
    """

    def __init__(self):
        """
        Initializes the scene manager with an empty scenes dictionary
        and current set to 0.
        """
        self.scenes: dict[Union[str, int], Scene] = {}
        self.__min_id = 0
        self.current = 0

    @property
    def is_empty(self) -> bool:
        """
        Checks if the scene manager contains no scene.

        Returns:
            bool: True if the scene is empty. False otherwise.
        """
        return not bool(self.scenes.keys())

    @property
    def current_scene(self) -> Scene:
        """
        Gets the current scene.

        Returns:
            Scene: The current scene.
        """
        return self.scenes.get(self.current)

    def add(self,
            scene: Scene,
            scene_id: Union[str, int] = None) -> Union[str, int]:
        """
        Add a scene to the current scene manager.

        Args:
            scene: The scene to add to the manager.
            scene_id: The id of the scene. Defaults to None.

        Raises:
            IdError: The given scene id is already used.

        Returns:
            Union[str, int]: Returns the id of the added scene.
        """
        if scene_id is None:
            scene_id = self.__min_id
            self.__min_id += 1

        if scene_id in self.scenes:
            raise IdError(
                f"The scene id {scene_id} is not unique in this manager")

        self.scenes[scene_id] = scene
        scene.id = scene_id
        return scene_id

    def set(self, scene_id: Union[str, int]):
        """
        Changes the current scene.

        Args:
            scene_id: The id of the new scene.
        """
        self.current = scene_id

    def draw(self):
        """Calls the draw function of the current scene."""
        if self.is_empty: return
        self.current_scene.private_draw()

    def update(self):
        """
        Calls the update function of the current scene.
        """
        if self.is_empty: return
        self.current_scene.private_update()

    def fixed_update(self):
        """Calls the fixed update function of the current scene."""
        if self.is_empty: return
        self.current_scene.private_fixed_update()
