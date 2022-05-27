"""
The Scene Manager houses a collection of scenes and allows switching between scenes.
It also handles drawing and updating the current scene.
"""
from typing import Dict

from . import Scene
from .. import IdError


# THIS IS A STATIC CLASS
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
    def current(cls) -> Scene | None:
        """
        The current scene.

        Returns:
            The current scene or none if there are no scenes in the manager.
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
    def remove(cls, scene: str | Scene):
        """
        Removes a Scene from the SceneManager.

        Args:
            scene: The id of the scene or the reference of the scene to remove.

        Raises:
            IdError: The given scene id is not in the manager.
        """
        if isinstance(scene, Scene):
            scene_id = scene.id
        else:
            scene_id = scene

        if scene_id in cls.scenes:
            del cls.scenes[scene_id]
            cls._current = ""
        else:
            raise IdError(f"The scene id {scene_id} is not in this manager")

    @classmethod
    def set(cls, scene_id: str):
        """
        Changes the current scene.

        Args:
            scene_id (str): The id of the new scene.
        """
        cls._current = scene_id

    @classmethod
    def setup(cls):
        """Calls the setup function of the current scene."""
        if cls.is_empty():
            return
        cls.current.private_setup()

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
