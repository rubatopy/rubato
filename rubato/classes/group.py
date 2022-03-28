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
        self.groups: List["Group"] = []
        self.game_objects: List[GameObject] = []
        self.z_index: int = param["z_index"]

    def add(self, *items: Union[GameObject, "Group"]):
        """
        Adds an item to the group.

        Args:
            items: The item(s) you wish to add to the group

        Raises:
            Error: The item being added is the group itself. A group cannot be
                added to itself.
            ValueError: The group can only hold game objects or other groups.
        """
        for item in items:
            if isinstance(item, GameObject):
                self.add_game_obj(item)
            elif isinstance(item, Group):
                self.add_group(item)
            else:
                raise ValueError(f"The group {self.name} can only hold game objects/groups.")

    def add_group(self, g: "Group"):
        if self == g:
            raise Error("Cannot add a group to itself.")
        if g.name == "":
            g.name = f"Group {len(self.groups)}"
        self.groups.append(g)

    def add_game_obj(self, g: GameObject):
        if g.name == "":
            g.name = f"Game Object {len(self.game_objects)}"
        self.game_objects.append(g)

    def remove(self, item: Union["GameObject", "Group"]):
        """
        Removes an item from the group.

        Args:
            item: The item to remove from the group.

        Raises:
            ValueError: The item is not in the group and cannot be deleted.
        """
        try:
            if isinstance(item, GameObject):
                self.game_objects.remove(item)
            elif isinstance(item, Group):
                self.groups.remove(item)
        except ValueError as e:
            raise ValueError(f"The item {item.name} is not in the group {self.name}") from e

    def setup(self):
        for group in self.groups:
            group.setup()
        for game_obj in self.game_objects:
            game_obj.setup()

    def update(self):
        for group in self.groups:
            group.update()
        for game_obj in self.game_objects:
            game_obj.update()

    def fixed_update(self):
        for group in self.groups:
            group.fixed_update()

        hitboxes: List[Hitbox] = []
        for game_obj in self.game_objects:
            game_obj.fixed_update()

            if hts := game_obj.get_all(Hitbox):
                for ht in hts:
                    for hitbox in hitboxes:
                        ht.collide(hitbox)
                hitboxes.extend(hts)

    def draw(self):
        self.groups.sort(key=lambda i: i.z_index)
        for group in self.groups:
            group.draw()

        self.game_objects.sort(key=lambda i: i.z_index)
        for game_obj in self.game_objects:
            game_obj.draw()
