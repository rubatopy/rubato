"""Miscellaneous helper functions for rubato developers."""

from . import Vector, GameObject, Component

def wrap(
    comp: Component,
    name: str = "",
    pos: Vector = Vector(),
    rotation: float = 0,
    z_index: int = 0,
    debug: bool = False
):
    """Automatically creates a gameobject surrounding a component and returns it."""
    return GameObject(name=name, pos=pos, rotation=rotation, z_index=z_index, debug=debug).add(comp)
