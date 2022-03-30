"""
The Scene class which is a collection of groups. It also houses the current
scene camera. Scenes come with a default group that everything is added to if
no other groups are specified.
"""
from typing import Union

from rubato.classes import Camera, Group, GameObject


class Scene:
    """
    A scene is a collection of groups.

    Attributes:
        root (Group): The base group of game objects in the scene.
        camera (Camera): The camera of this scene.
        id (str): The id of this scene.
    """

    def __init__(self):
        """
        Initializes a scene with an empty collection of game objects, a new camera,
        and a blank id.
        """
        self.root: Group = Group({"name": "root"})
        self.camera = Camera()
        self.id: str = ""

    def add(self, *items: Union[GameObject, "Group"]):
        """
        Adds an item to the root group.

        Args:
            item: The item or list of items to add.

        """
        self.root.add(*items)

    def remove(self, item: Union[GameObject, "Group"]):
        """
        Removes an item from the root group.

        Args:
            item: The item to remove.

        """
        self.root.remove(item)

    def private_draw(self):
        self.draw()
        self.root.draw()

    def private_update(self):
        self.update()
        self.root.update()

    def private_fixed_update(self):
        self.fixed_update()
        self.root.fixed_update()

    def private_setup(self):
        self.setup()
        self.root.setup()

    def setup(self):
        """The start loop for this scene. It is run before the first frame."""
        pass

    def draw(self):
        """
        The draw loop for this scene. Is empty by default an can be
        overridden.
        """
        pass

    def update(self):
        """
        The update loop for this scene. Is empty by default an can be
        overridden.
        """
        pass

    def fixed_update(self):
        """
        The fixed update loop for this scene. Is empty by default an can be
        overridden.
        """
        pass

    def paused_update(self):
        """
        A function that will be run ever frame whether or not the game is
        currently paused. Should be overriden.
        """
        pass
