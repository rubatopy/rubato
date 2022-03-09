"""
Groups contain sprites and allow specific sprites to be seperated.
"""

from typing import List, Tuple, Union, TYPE_CHECKING
from rubato.utils.error import Error
from rubato.classes.components import Hitbox

if TYPE_CHECKING:
    from rubato.classes import Sprite


class Group:
    """A group of sprites"""

    def __init__(self) -> None:
        self.items: List[Union["Sprite", Group]] = []

    def add(self, item: Union["Sprite", "Group"]):
        """
        Adds an item to the group.

        Args:
            item: The item to add to the group.

        Raises:
            Error: The item being added is the group itself. A group cannot be
                added to itself.
        """
        if self != item:
            self.items.append(item)
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
            i = self.items.index(item)
            del self.items[i]
        except ValueError as e:
            raise ValueError("This item is not in this group") from e

    def update(self):
        for item in self.items:
            item.update()

    def fixed_update(self):
        hitboxes: List["Hitbox"] = []
        for item in self.items:
            if (ht := item.get_component(Hitbox)) is not None:
                hitboxes.append(ht)

            item.fixed_update()

        pairs: List[Tuple["Hitbox", "Hitbox"]] = []

        for hitbox_a in hitboxes:
            for hitbox_b in hitboxes:
                if hitbox_a != hitbox_b:
                    if not ((hitbox_a, hitbox_b) in pairs or
                            (hitbox_b, hitbox_a) in pairs):
                        pairs.append((hitbox_a, hitbox_b))

        for pair in pairs:
            pair[0].collide(pair[1])

    def draw(self):
        for item in self.items:
            item.draw()
