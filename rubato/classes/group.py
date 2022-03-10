"""
Groups contain sprites and allow specific sprites to be seperated.
"""

from typing import List, Union
from rubato.utils.error import Error
from rubato.classes import Sprite
from rubato.classes.components import Hitbox


class Group:
    """A group of sprites"""

    def __init__(self) -> None:
        self.items: List[Union[Sprite, "Group"]] = []

    def add(self, item: Union[Sprite, "Group", List[Union[Sprite, "Group"]]]):
        """
        Adds an item to the group.

        Args:
            item: The item or list of items to add to the group.

        Raises:
            Error: The item being added is the group itself. A group cannot be
                added to itself.
        """
        if self != item:
            if isinstance(item, list):
                for it in item:
                    self.add(it)
            else:
                return self.items.append(item)
        else:
            raise Error("Cannot add a group to itself.")

    def remove(self, item: Union["Sprite", "Group"]):
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
            raise ValueError("This item is not in this group") from e

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

            if isinstance(item, Sprite) and \
                (ht := item.get_component(Hitbox)) is not None:
                for hitbox in hitboxes:
                    ht.collide(hitbox)
                hitboxes.append(ht)


    def draw(self):
        for item in self.items:
            item.draw()
