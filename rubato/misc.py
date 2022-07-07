"""Miscellaneous helper functions for rubato developers."""
from typing import List

from . import Vector, GameObject, Component

def wrap(
    comp: Component | List[Component],
    name: str = "",
    pos: Vector = Vector(),
    rotation: float = 0,
    z_index: int = 0,
    debug: bool = False
):
    """
    Wraps a component or list of components in a GameObject.

    Args:
        comp (Component | List[Component]): The component or list of components to wrap.
        name (str, optional): The name of the GameObject. Defaults to "".
        pos (Vector, optional): The position of the GameObject. Defaults to Vector().
        rotation (float, optional): The rotation of the GameObject. Defaults to 0.
        z_index (int, optional): The z_index of the GameObject. Defaults to 0.
        debug (bool, optional): Whether the GameObject is in debug mode. Defaults to False.

    Raises:
        TypeError: If comp is not a Component or a list of Components.

    Returns:
        GameObject: The wrapped GameObject.
    """
    go = GameObject(name=name, pos=pos, rotation=rotation, z_index=z_index, debug=debug)
    if isinstance(comp, Component):
        go.add(comp)
    elif isinstance(comp, list):
        for c in comp:
            go.add(c)
    else:
        raise TypeError("comp must be a Component or a list of Components.")
    return go
