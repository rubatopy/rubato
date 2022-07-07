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
    """Automatically creates a gameobject surrounding a component and returns it."""
    go = GameObject(name=name, pos=pos, rotation=rotation, z_index=z_index, debug=debug)
    if isinstance(comp, Component):
        go.add(comp)
    elif isinstance(comp, list):
        for c in comp:
            go.add(c)
    else:
        raise TypeError("comp must be a Component or a list of Components.")
    return go
