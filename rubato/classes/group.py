"""
Groups contain game objects and allow specific game objects to be seperated.
"""

from typing import List, Union
from rubato.utils import Error, Defaults
from rubato.classes import GameObject
from rubato.classes.components import Hitbox


class Group:
    """A group of game objects"""

    def __init__(self, options: dict = {}) -> None:
        param = Defaults.group_defaults | options
        self.name: str = param["name"]
        self.items: List[Union[GameObject, "Group"]] = []
        self.z_index: int = param["z_index"]

    def add(self, *items: Union[GameObject, "Group"]):
        """
        Adds an item to the group.

        Args:
            items: The item(s) you wish to add to the group

        Raises:
            Error: The item being added is the group itself. A group cannot be
                added to itself.
        """
        for item in items:
            if self != item:
                if isinstance(item, Group):
                    if item.name == "":
                        item.name = f"Group {len(self.items)}"
                elif isinstance(item, GameObject):
                    if item.name == "":
                        item.name = f"Game Object {len(self.items)}"
                else:
                    raise ValueError(f"The group {self.name} can only hold game objects/groups.")
                self.items.append(item)
            else:
                raise Error("Cannot add a group to itself.")

    def remove(self, item: Union["GameObject", "Group"]):
        """
        Removes an item from the group.

        Args:
            item: The item to remove from the group.

        Raises:
            ValueError: The item is not in the group and cannot be deleted.
        """
        try:
            self.items.remove(item)
        except ValueError as e:
            raise ValueError(f"The item {item.name} is not in the group {self.name}") from e

    def setup(self):
        for item in self.items:
            item.setup()

    def update(self):
        for item in self.items:
            item.update()

    def fixed_update(self):
        hitboxes: List["Hitbox"] = []
        for item in self.items:
            item.fixed_update()

            if isinstance(item, GameObject) and len(hts := item.get_all(Hitbox)):
                for hitbox in hitboxes:
                    for ht in hts:
                        ht.collide(hitbox)
                hitboxes += [*hts]

    def draw(self):
        self.items.sort(key=lambda i: i.z_index)

        for item in self.items:
            item.draw()
