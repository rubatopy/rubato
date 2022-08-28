"""A simple particle."""
from dataclasses import dataclass
from typing import Callable

from ... import Surface
from .... import Vector, Time, Draw, Camera


@dataclass(repr=False, slots=True, unsafe_hash=True)
class Particle:

    movement: Callable[["Particle", float], None]
    velocity: Vector | tuple[float, float]  # pyright: ignore [reportGeneralTypeIssues]
    pos: Vector | tuple[float, float]  # pyright: ignore [reportGeneralTypeIssues]
    rotation: float
    scale: float
    surface: Surface
    life: float
    z_index: int

    def __post_init__(self):
        self.velocity: Vector = Vector.create(self.velocity)
        self.pos: Vector = Vector.create(self.pos)

    def fixed_update(self):
        self.life -= Time.fixed_delta
        self.movement(self, Time.fixed_delta)

    def draw(self, camera: Camera):
        self.surface.rotation = self.rotation
        Draw.queue_surface(self.surface, self.pos, self.z_index, camera)
