"""
Groups contain game objects or other groups and allow separation between game objects.
"""
from __future__ import annotations

from . import GameObject, Hitbox, QTree
from .. import Error, Camera


class Group:
    """
    A divider between separate categories of game objects.
    Can be used to differentiate between different "groups" of elements that you don't want to interact;
    i.e. you don't want a gameobject representing an enemy to collide with the coins in the scene.

    Args:
        name: The name of the group. Defaults to "" and is set to "Group #" when it is added to another Group or Scene.
        active: Whether the group is active or not. Defaults to True.
        hidden: Whether the group is hidden or not. Defaults to False.
    """

    def __init__(self, name: str = "", active: bool = True, hidden: bool = False):
        self.name: str = name
        """The name of the group."""
        self.active: bool = active
        """Whether to update and draw this group's contents."""
        self.groups: list[Group] = []
        """A list of groups that are children of this group."""
        self.game_objects: list[GameObject] = []
        """A list of game objects that are children of this group."""
        self.hidden: bool = hidden
        """Whether to hide (not draw) this group's contents."""

    def add(self, *items: GameObject | Group):
        """
        Adds an item to the group.

        Args:
            items: The item(s) you wish to add to the group

        Raises:
            Error: The item being added is already in the group.
            ValueError: The group can only hold game objects or other groups.

        Returns:
            Group: This group.
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

    def remove(self, item: GameObject | Group) -> bool:
        """
        Remove an item shallowly from the group.

        Args:
            item: The group or gameobject to remove.

        Returns:
            Whether it was removed successfully.
        """
        success = True
        try:
            if isinstance(item, GameObject):
                self.game_objects.remove(item)
            elif isinstance(item, Group):
                self.groups.remove(item)
        except ValueError:
            success = False
        return success

    def update(self):
        if not self.active:
            return

        for group in self.groups:
            group.update()
        for game_obj in self.game_objects:
            game_obj.update()

    def fixed_update(self):
        """
        Runs a physics iteration on the group.
        Called automatically by rubato as long as the group is added to a scene.
        """
        if not self.active:
            return

        for group in self.groups:
            group.fixed_update()

        all_hts = []
        for game_obj in self.game_objects:
            game_obj.fixed_update()
            hts = game_obj.get_all(Hitbox)
            if hts:
                all_hts.append(hts)

        qtree = QTree(all_hts)

        for go in self.all_gameobjects():
            hts = go.get_all(Hitbox)
            if hts:
                qtree.collide(hts, qtree.calc_bb(hts))

    def all_gameobjects(self, include_self: bool = False) -> list[GameObject]:
        """
        Returns a list of all game objects in the group and all of its children.

        Args:
            include_self (bool, optional): Whether to include this group's direct children. Defaults to False.

        Returns:
            list[GameObject]: The resultant list.
        """
        ret: list[GameObject] = self.game_objects if include_self else []
        for group in self.groups:
            ret.extend(group.all_gameobjects(True))
        return ret

    def draw(self, camera: Camera):
        if not self.active or self.hidden:
            return

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
