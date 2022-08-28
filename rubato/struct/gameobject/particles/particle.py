"""A simple particle."""
from dataclasses import dataclass
from typing import Callable

from ... import Surface
from .... import Vector, Time, Draw, Camera


@dataclass(repr=False, slots=True, unsafe_hash=True)
class Particle:
    """A simple particle."""

    movement: Callable[["Particle", float], None]
    velocity: Vector | tuple[float, float]  # pyright: ignore [reportGeneralTypeIssues]
    pos: Vector | tuple[float, float]  # pyright: ignore [reportGeneralTypeIssues]
    rotation: float
    scale: float
    surface: Surface
    lifespan: float
    z_index: int
    age: float = 0

    def __post_init__(self):
        self.velocity: Vector = Vector.create(self.velocity)
        self.pos: Vector = Vector.create(self.pos)

    def _fixed_update(self):
        self.age += Time.fixed_delta
        self.movement(self, Time.fixed_delta)

    def _draw(self, camera: Camera):
        self.surface.rotation = self.rotation
        Draw.queue_surface(self.surface, self.pos, self.z_index, camera)
