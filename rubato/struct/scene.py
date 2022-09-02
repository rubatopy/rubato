"""
An abstraction for a "level", or scene, in rubato.
"""
from __future__ import annotations

from . import Group, GameObject
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
        self.root: Group = Group(name="root")
        """The base group of game objects in the scene."""
        self.ui: Group = Group(name="ui")
        """
        The ui elements of this scene. These are drawn on top of everything else and do not interact with the other
        game objects.
        """
        self.camera = Camera()
        """The camera of this scene."""
        self._ui_cam = Camera()
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

    def add(self, *items: GameObject | Group):
        """
        Adds an item to the root group.

        Args:
            *items: The items to add to the scene.
        """
        self.root.add(*items)

    def add_ui(self, *items: GameObject):
        """
        Adds Game Objects as UI to the scene. When a game object is added as a UI, they draw as they normally would, but
        they don't collide with other game objects, they draw on top of everything else, and they are unaffected by the
        camera.

        Args:
            *items: The items to add to the scene.
        """
        self.ui.add(*items)

    def remove(self, item: GameObject | Group) -> bool:
        """
        Removes an item from the root group.

        Args:
            item: The item to remove.

        Returns:
            Whether it was removed successfully.
        """
        return self.root.remove(item)

    def remove_ui(self, item: GameObject) -> bool:
        """
        Removes an item from the ui group.

        Args:
            item: The item to remove.

        Returns:
            Whether it was removed successfully.
        """
        return self.ui.remove(item)

    def _setup(self):
        self.started = True
        self.setup()

    def _update(self):
        if not self.started:
            self._setup()

        self.update()
        self.root.update()
        self.ui.update()

    def _paused_update(self):
        if not self.started:
            self._setup()

        self.paused_update()

    def _fixed_update(self):
        self.fixed_update()
        self.root.fixed_update()
        self.ui.fixed_update()

    def _draw(self):
        Draw.clear(self.background_color, self.border_color)
        self.draw()
        self.root.draw(self.camera)
        self.ui.draw(self._ui_cam)

    def setup(self):
        """
        The start loop for this scene. It is run before the first frame.
        Is empty be default and can be overriden.
        """
        pass

    def update(self):
        """
        The update loop for this scene. It is run once every frame, before :meth:`draw`.
        Is empty by default an can be overridden.
        """
        pass

    def fixed_update(self):
        """
        The fixed update loop for this scene. It is run (potentially) many times a frame.
        Is empty by default an can be overridden.

        Note:
            You should define fixed_update only for high priority calculations that need to match the physics fps.
        """
        pass

    def paused_update(self):
        """
        The paused update loop for this scene. It is run once a frame when the game is paused.
        Is empty by default an can be overridden.
        """
        pass

    def draw(self):
        """
        The draw loop for this scene. It is run once every frame.
        Is empty by default an can beoverridden.
        """
        pass

    def clone(self) -> Scene:
        """
        Clones this scene.

        Warning:
            This is a relatively expensive operation as it clones every group in the scene.
        """
        new_scene = Scene(
            name=f"{self.name} (clone)", background_color=self.background_color, border_color=self.border_color
        )
        new_scene.root = self.root.clone()
        new_scene.ui = self.ui.clone()

        return new_scene
