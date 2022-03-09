"""
THe Scene class which is a collection of groups. It also houses the current
scene camera. Scenes come with a default group that everything is added to if
no other groups are specified.
"""
from typing import List, Union, TYPE_CHECKING
from rubato.classes import Camera, Group
from rubato.utils.error import Error

if TYPE_CHECKING:
    from rubato.classes import Sprite


class Scene:
    """
    A scene is a collection of groups.

    Attributes:
        groups (List[Group]): The collection
            of groups housed in this scene.
        camera (Camera): The camera of this scene.
        id (str): The id of this scene.
    """

    def __init__(self):
        """
        Initializes a scene with an empty collection of sprites, a new camera,
        and a blank id.
        """
        self.groups: List["Group"] = [Group()]
        self.camera = Camera()
        self.id: str = ""

    def add_group(self, group: "Group"):
        """
        Adds a group to the scene.

        Args:
            group: The group to add.

        Raises:
            Warning: The group you tried to add was already in the scene. This
                group will not be added twice.
        """
        if group not in self.groups:
            self.groups.append(group)
        else:
            raise Warning(
                f"The group {group} is already in the scene." + \
                    "(it was not added twice)"
            )

    def remove_group(self, group: "Group"):
        """
        Removes a group from the scene.

        Args:
            group: The group to remove.

        Raises:
            ValueError: The group could not be found in this scene and was
                therefore not removed.
        """
        try:
            i = self.items.index(group)
            del self.items[i]
        except ValueError as e:
            raise ValueError("This group is not in this scene") from e

    def add_item(self, item: Union["Sprite", "Group"]):
        """
        Adds an item to the default group.

        Args:
            item: The item to add.

        Raises:
            Error: The default group was either deleted or could not be found
                and therefore the item was not added.
        """
        if len(self.groups) > 0:
            self.groups[0].add(item)
        else:
            raise Error(
                "The default group was deleted and the item was not added")

    def remove_item(self, item: Union["Sprite", "Group"]):
        """
        Removes an item from the default group.

        Args:
            item: The item to remove.

        Raises:
            Error: The default group was delete and the item was not removed.
        """
        if len(self.groups) > 0:
            self.groups[0].remove(item)
        else:
            raise Error(
                "The default group was deleted and the item was not removed")

    def private_draw(self):
        for group in self.groups:
            group.draw()

    def private_update(self):
        self.update()
        for group in self.groups:
            group.update()

    def private_fixed_update(self):
        self.fixed_update()
        for group in self.groups:
            group.fixed_update()

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
