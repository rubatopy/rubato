"""
An abstraction for a "level", or scene, in rubato.
"""
from __future__ import annotations

from . import GameObject, Hitbox
from .gameobject.physics.qtree import _QTree
from .. import Game, Color, Draw, Camera


class Scene:
    """
    A scene divides different, potentially unrelated, sections of a game into groups.
    For instance, there may be a scene for the main menu, a scene for each level, and a scene for the win screen.

    Args:
        name: The name of the scene. This is used to reference the scene. Automatically set if not assigned.
            Once this is set, it cannot be changed.
        background_color: The color of the background of the window. Defaults to Color(255, 255, 255).
        border_color: The color of the border of the window. Defaults to Color(0, 0, 0).
    """

    def __init__(
        self,
        name: str | None = None,
        background_color: Color = Color.white,
        border_color: Color = Color.black,
    ):
        self._root: list[GameObject] = []
        """The list of gameobjects in this scene."""
        self._add_queue: list[GameObject] = []
        """A buffer for gameobjects that will be added on the next frame."""
        self.camera = Camera()
        """The camera of this scene."""
        self.started = False
        self.border_color = border_color
        """The color of the border of the window."""
        self.background_color = background_color
        """The color of the background of the window."""

        self.__id = Game._add(self, name)

    @property
    def name(self):
        """
        The name of this scene. Read-only.
        """
        return self.__id

    def switch(self):
        """
        Switches to this scene on the next frame.
        """
        Game.set_scene(self.name)

    def add(self, *gos: GameObject):
        """
        Adds gameobject(s) to the scene.

        Args:
            *gos: The gameobjects to add to the scene.
        """
        self._add_queue.extend(gos)

    def remove(self, *gos: GameObject) -> bool:
        """
        Removes gameobject(s) from the scene. This will return false if any of the gameobjects are not in the scene,
        but it will guarantee that all the gameobjects are removed.

        Args:
            *gos: The gameobjects to remove.

        Returns:
            True if all gameobjects were present in the scene, False otherwise.
        """
        success: bool = True
        for go in gos:
            if go in self._add_queue:
                self._add_queue.remove(go)
            else:
                try:
                    self._root.remove(go)
                except ValueError:
                    success = False
        return success

    def _dump(self):
        self._root.extend(self._add_queue)
        self._add_queue.clear()

    def _setup(self):
        self.started = True
        self.setup()

    def _update(self):
        if not self.started:
            self._setup()

        self.update()

        for go in self._root:
            go._update()

    def _paused_update(self):
        if not self.started:
            self._setup()

        self.paused_update()

    def _fixed_update(self):
        self.fixed_update()

        all_hts = []
        for go in self._root:
            go._fixed_update()
            hts = go._deep_get_all(Hitbox)
            if hts:
                all_hts.append(hts)

        _QTree(all_hts)

    def _draw(self):
        Draw.clear(self.background_color, self.border_color)
        self.draw()

        for go in self._root:
            if go.z_index <= self.camera.z_index:
                go._draw(self.camera)

    def setup(self):
        """
        The start loop for this scene. It is run before the first frame.
        Is empty be default and can be overriden.
        """
        pass

    def update(self):
        """
        The update loop for this scene. It is run once every frame, before :meth:`draw`.
        Is empty by default and can be overridden.
        """
        pass

    def fixed_update(self):
        """
        The fixed update loop for this scene. It is run (potentially) many times a frame.
        Is empty by default and can be overridden.

        Note:
            You should define fixed_update only for high priority calculations that need to match the physics fps.
        """
        pass

    def paused_update(self):
        """
        The paused update loop for this scene. It is run once a frame when the game is paused.
        Is empty by default and can be overridden.
        """
        pass

    def draw(self):
        """
        The draw loop for this scene. It is run once every frame.
        Is empty by default and can be overridden.
        """
        pass

    def on_switch(self):
        """
        An overridable method that is called whenever this scene is switched to.
        """
        pass

    def clone(self) -> Scene:
        """
        Clones this scene.

        Warning:
            This is a relatively expensive operation as it clones every gameobject in the scene.
        """
        new_scene = Scene(
            name=f"{self.name} (clone)", background_color=self.background_color, border_color=self.border_color
        )
        new_scene._root = [go.clone() for go in self._root]
        new_scene._add_queue = [go.clone() for go in self._add_queue]

        return new_scene

    def contains(self, go: GameObject) -> bool:
        """
        Checks if the scene contains a gameobject.

        Args:
            go: The gameobject to check for.
        """
        return go in self._root or go in self._add_queue
