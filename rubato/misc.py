"""
Miscellaneous helper functions for rubato developers.
"""
from typing import Sequence
from . import Vector, GameObject, Component, Game, Input


def world_mouse() -> Vector:
    """
    Returns the mouse position in world-coordinates.

    Returns:
        Vector: The mouse position in world coordinates.
    """
    if Game._current != "":
        return Game.current().camera.i_transform(Input.get_mouse_pos())
    return Input.get_mouse_pos()


def wrap(
    comp: Component | Sequence[Component],
    pos: Vector | tuple[float, float] = (0, 0),
    rotation: float = 0,  # test: skip
    z_index: int = 0,
    ignore_cam: bool = False,
    parent: GameObject | None = None,
    name: str = "",
    debug: bool = False,
    active: bool = True,
    hidden: bool = False,
):
    """
    Wraps a component or list of components in a GameObject.

    Args:
        comp: The component or list of components to wrap.
        pos: The position of the GameObject. Defaults to (0, 0).
        rotation: The rotation of the GameObject. Defaults to 0.
        z_index: The z_index of the GameObject. Defaults to 0.
        ignore_cam: Whether the GameObject ignores the scene's camera when drawing or not. Defaults to False.
        parent: The parent GameObject of the GameObject. Defaults to None.
        name: The name of the GameObject. Defaults to "".
        debug: Whether the GameObject is in debug mode. Defaults to False.
        active: Whether the GameObject is active. Defaults to True.
        hidden: Whether the GameObject is hidden. Defaults to False.

    Raises:
        TypeError: If comp is not a Component or a list of Components.

    Returns:
        The wrapped GameObject.
    """
    go = GameObject(
        pos=pos,
        rotation=rotation,
        z_index=z_index,
        ignore_cam=ignore_cam,
        parent=parent,
        name=name,
        debug=debug,
        active=active,
        hidden=hidden
    )
    if isinstance(comp, Component):
        go.add(comp)
    elif isinstance(comp, list):
        go.add(*comp)
    else:
        raise TypeError("comp must be a Component or a list of Components.")
    return go
