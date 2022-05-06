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

    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self._current: str = ""

    @property
    def current(self) -> Scene:
        """
        The current scene.

        Returns:
            The current scene.
        """
        return self.scenes.get(self._current)

    def is_empty(self) -> bool:
        """
        Checks if the scene manager contains no scene.

        Returns:
            bool: True if the scene is empty. False otherwise.
        """
        return not self.scenes

    def add(self, scene: Scene, scene_id: str):
        """
        Add a scene to the current scene manager.
        If the manager is empty the current scene will be updated.

        Args:
            scene (Scene): The scene to add to the manager.
            scene_id (str): The id of the scene.

        Raises:
            IdError: The given scene id is already used.
        """
        if scene_id in self.scenes:
            raise IdError(f"The scene id {scene_id} is not unique in this manager")

        if self.is_empty():
            self.set(scene_id)

        self.scenes[scene_id] = scene
        scene.id = scene_id

    def add_new(self, scene_id: str = "") -> Scene:
        """
        Add a scene to the current scene manager.
        If the manager is empty the current scene will be updated.

        Args:
            scene_id (str): The id of the scene.

        Raises:
            IdError: The given scene id is already used.

        Returns:
            Scene: The added scene.
        """
        scene = Scene()
        if scene_id == "":
            scene_id = len(self.scenes)
        if scene_id in self.scenes:
            raise IdError(f"The scene id {scene_id} is not unique in this manager")

        if self.is_empty():
            self.set(scene_id)

        self.scenes[scene_id] = scene
        scene.id = scene_id

        return scene

    def set(self, scene_id: str):
        """
        Changes the current scene.

        Args:
            scene_id (str): The id of the new scene.
        """
        self._current = scene_id

    def setup(self):
        """Calls the setup function of the current scene."""
        if self.is_empty():
            return
        self.current.private_setup()

    def draw(self):
        """Calls the draw function of the current scene."""
        if self.is_empty():
            return
        self.current.private_draw()

    def update(self):
        """Calls the update function of the current scene."""
        if self.is_empty():
            return
        self.current.private_update()

    def fixed_update(self):
        """Calls the fixed update function of the current scene."""
        if self.is_empty():
            return
        self.current.private_fixed_update()

    def paused_update(self):
        """Calls the paused update function of the current scene."""
        if self.is_empty():
            return
        self.current.paused_update()
