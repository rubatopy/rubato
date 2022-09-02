"""A simple particle."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

from ... import Surface
from .... import Vector


@dataclass(repr=False, slots=True, unsafe_hash=True)
class Particle:
    """
    A simple particle.

    Args:
        movement: The movement function of a particle.
        velocity: The velocity of the particle.
        pos: The position of the particle.
        rotation: The rotation of the particle.
        scale: The scale of the particle.
        surface: The surface of the particle.
        lifespan: The lifespan of the particle.
        z_index: The z-index of the particle.
        age: The age of the particle. Defaults to 0.
    """

    movement: Callable[[Particle, float], None]
    """The movement function of the particle"""
    velocity: Vector | tuple[float, float]  # pyright: ignore [reportGeneralTypeIssues]
    """The velocity of the particle."""
    pos: Vector | tuple[float, float]  # pyright: ignore [reportGeneralTypeIssues]
    """The position of the particle."""
    rotation: float
    """The rotation of the particle."""
    scale: float
    """The scale of the particle."""
    surface: Surface
    """The surface that renders the particle."""
    lifespan: float
    """The lifespan of the particle. (in seconds)"""
    z_index: int
    """The z index of the particle."""
    age: float = 0
    """The age of the particle. (in seconds)"""
    _original_scale: Vector | None = field(init=False)  # pyright: ignore [reportGeneralTypeIssues]
    _system_pos: Vector = field(default_factory=Vector, init=False)
    _system_rotation: float = field(default=0, init=False)
    _system_z: int = field(default=0, init=False)

    def __post_init__(self):
        self.velocity: Vector = Vector.create(self.velocity)
        self.pos: Vector = Vector.create(self.pos)
        self._original_scale: Vector = self.surface.scale.clone()
