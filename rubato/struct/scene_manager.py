"""
The Scene Manager houses a collection of scenes and allows switching between scenes.
It also handles drawing and updating the current scene.
"""
from typing import Dict

from . import Scene
from .. import IdError

class SceneManager:
    """
    The Scene Manager contains and handle multiple scenes.

    Attributes:
        scenes (Dict[str, Scene]): The collection of scenes in the
            manager. Accessed by scene id.
    """

    scenes: Dict[str, Scene] = {}
    _current: str = ""

    @classmethod
    @property
    def current(cls) -> Scene:
        """
        The current scene.

        Returns:
            The current scene.
        """
        return cls.scenes.get(cls._current)

    @classmethod
    def is_empty(cls) -> bool:
        """
        Checks if the scene manager contains no scene.

        Returns:
            bool: True if the scene is empty. False otherwise.
        """
        return not cls.scenes

    @classmethod
    def add(cls, scene: Scene, scene_id: str):
        """
        Add a scene to the current scene manager.
        If the manager is empty the current scene will be updated.

        Args:
            scene (Scene): The scene to add to the manager.
            scene_id (str): The id of the scene.

        Raises:
            IdError: The given scene id is already used.
        """
        if scene_id in cls.scenes:
            raise IdError(f"The scene id {scene_id} is not unique in this manager")

        if cls.is_empty():
            cls.set(scene_id)

        cls.scenes[scene_id] = scene
        scene.id = scene_id

    @classmethod
    def set(cls, scene_id: str):
        """
        Changes the current scene.

        Args:
            scene_id (str): The id of the new scene.
        """
        cls._current = scene_id

    @classmethod
    def draw(cls):
        """Calls the draw function of the current scene."""
        if cls.is_empty():
            return
        cls.current.private_draw()

    @classmethod
    def update(cls):
        """Calls the update function of the current scene."""
        if cls.is_empty():
            return
        cls.current.private_update()

    @classmethod
    def fixed_update(cls):
        """Calls the fixed update function of the current scene."""
        if cls.is_empty():
            return
        cls.current.private_fixed_update()

    @classmethod
    def paused_update(cls):
        """Calls the paused update function of the current scene."""
        if cls.is_empty():
            return
        cls.current.paused_update()
