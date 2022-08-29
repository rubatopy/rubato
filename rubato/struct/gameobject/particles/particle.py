"""A simple particle."""
from dataclasses import dataclass
from typing import Callable

from ... import Surface
from .... import Vector, Time, Draw, Camera


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

    movement: Callable[["Particle", float], None]
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

    def __post_init__(self):
        self.velocity: Vector = Vector.create(self.velocity)
        self.pos: Vector = Vector.create(self.pos)

    def fixed_update(self):
        """A particle's fixed update functions"""
        self.age += Time.fixed_delta
        self.movement(self, Time.fixed_delta)

    def draw(self, camera: Camera):
        """A particle's draw function."""
        self.surface.rotation = self.rotation
        Draw.queue_surface(self.surface, self.pos, self.z_index, camera)

    def delete(self):
        """Deletes a particle."""
        self.surface.delete()
