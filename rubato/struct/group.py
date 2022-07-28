"""
Groups contain game objects or other groups and allow separation between game objects.
"""
from __future__ import annotations
from typing import List

from . import GameObject, Hitbox, QTree
from .. import Error, Display, Camera


class Group:
    """
    The group class implementation.

    Args:
        name: The name of the group. Defaults to "" and is set to "Group #" when it is added to another Group or Scene.
        active: Whether the group is active or not. Defaults to True.

    Attributes:
        name (str): The name of the group.
        active (bool): Whether the group is active or not.
        groups (List[Group]): A list of groups that are children of this group.
        game_objects (List[GameObject]): A list of game objects that are children of this group.
    """

    def __init__(self, name: str = "", active: bool = True):
        self.name: str = name
        self.active: bool = active
        self.groups: List[Group] = []
        self.game_objects: List[GameObject] = []

    def add(self, *items: GameObject | Group):
        """
        Adds an item to the group.

        Args:
            items: The item(s) you wish to add to the group

        Raises:
            Error: The item being added is already in the group.
            ValueError: The group can only hold game objects or other groups.

        Returns:
            GameObject: The current game object
        """
        for item in items:
            if self.contains(item):
                raise Error(f"The group {self.name} already contains {item.name}.")
            if isinstance(item, GameObject):
                self.add_game_obj(item)
            elif isinstance(item, Group):
                self.add_group(item)
            else:
                raise ValueError(f"The group {self.name} can only hold game objects/groups.")

        return self

    def add_group(self, g: Group):
        """Add a group to the group."""
        if self == g:
            raise Error("Cannot add a group to itself.")
        if g.name == "":
            g.name = f"Group {len(self.groups)}"
        self.groups.append(g)

    def add_game_obj(self, g: GameObject):
        """Add a game object to the group"""
        if g.name == "":
            g.name = f"Game Object {len(self.game_objects)}"
        self.game_objects.append(g)

    def delete(self, item: GameObject | Group):
        """
        Removes an item from the group.

        Args:
            item: The item to remove from the group.

        Note:
            The actually game object is not deleted, just removed from the group.

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

    def update(self):
        if self.active:
            for group in self.groups:
                group.update()
            for game_obj in self.game_objects:
                game_obj.update()

    def fixed_update(self):
        """
        Runs a physics iteration on the group.
        Called automatically by rubato as long as the group is added to a scene.
        """
        if self.active:
            for game_obj in self.game_objects:
                game_obj.fixed_update()

            qtree = QTree(Display.top_left, Display.bottom_right)

            # collide all hitboxes with each other
            for game_obj in self.game_objects:
                if hts := game_obj._components.get(Hitbox, []):  # pylint: disable=protected-access
                    bb = QTree.calc_bb(hts)
                    qtree.collide(hts, bb)
                    qtree.insert(hts, bb)

            for group in self.groups:
                group.fixed_update()

                # collide children groups with parent hitboxes
                for game_obj in group.game_objects:
                    if hts := game_obj._components.get(Hitbox, []):  # pylint: disable=protected-access
                        qtree.collide(hts, QTree.calc_bb(hts))

    def draw(self, camera: Camera):
        if self.active:
            for group in self.groups:
                group.draw(camera)

            for game_obj in self.game_objects:
                if game_obj.z_index <= camera.z_index:
                    game_obj.draw(camera)

    def count(self) -> int:
        """
        Counts all the GameObjects and subgroups in this group.
        Returns:
            int: The total number of GameObjects and subgroups contained in this group.
        """
        return len(self.game_objects) + len(self.groups) + sum([group.count() for group in self.groups])

    def clone(self) -> Group:
        """
        Clones the group and all of its children.

        Warning:
            This is a relatively expensive operation as it clones every game object and component in the group.
        """
        new_group = Group(f"{self.name} (clone)", self.active)

        for group in self.groups:
            new_group.add(group.clone())

        for game_obj in self.game_objects:
            new_group.add(game_obj.clone())

        return new_group

    def contains(self, other: GameObject | Group) -> bool:
        """
        Checks if the group contains the given object.

        Args:
            other: The object to check for.

        Returns:
            bool: Whether the group contains the object or not.
        """
        if isinstance(other, GameObject):
            return other in self.game_objects or sum([group.contains(other) for group in self.groups]) != 0

        if isinstance(other, Group):
            return other in self.groups or sum([group.contains(other) for group in self.groups]) != 0

        return False
