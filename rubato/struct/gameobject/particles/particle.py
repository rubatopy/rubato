"""A simple particle."""
from __future__ import annotations
from typing import Callable

from ... import Surface
from .... import Vector


class Particle:
    """
    A simple particle.

    Args:
        surface: The surface of the particle.
        movement: The movement function of a particle. Defaults to `Particle.default_movement`.
        velocity: The velocity of the particle. Defaults to (0, 0).
        acceleration: The acceleration of the particle. Defaults to (0, 0).
        pos: The position of the particle. Defaults to (0, 0).
        rotation: The rotation of the particle. Defaults to 0.
        rot_velocity: The rotational velocity of the particle. Defaults to 0.
        rot_acceleration: The rotational acceleration of the particle. Defaults to 0.
        scale: The scale of the particle. Defaults to 1.
        lifespan: The lifespan of the particle (in seconds). Defaults to 1.
        z_index: The z-index of the particle. Defaults to 0.
        age: The age of the particle (in seconds). Defaults to 0.
    """

    def __init__(
        self,
        surface: Surface,
        movement: Callable[[Particle, float], None] | None = None,
        pos: Vector | tuple[float, float] = (0, 0),
        velocity: Vector | tuple[float, float] = (0, 0),
        acceleration: Vector | tuple[float, float] = (0, 0),
        rotation: float = 0,
        rot_velocity: float = 0,
        rot_acceleration: float = 0,
        scale: float = 1,
        lifespan: float = 1,
        z_index: int = 0,
        age: float = 0,
    ) -> None:
        self.surface: Surface = surface
        """The surface that renders the particle."""
        self.movement: Callable[[Particle, float], None] = movement or Particle.default_movement
        """The movement function of the particle"""
        self.velocity: Vector = Vector.create(velocity)
        """The velocity of the particle."""
        self.acceleration: Vector = Vector.create(acceleration)
        """The acceleration of the particle."""
        self.pos: Vector = Vector.create(pos)
        """The position of the particle."""
        self.rotation: float = rotation
        """The rotation of the particle."""
        self.rot_velocity: float = rot_velocity
        """The rotational velocity of the particle."""
        self.rot_acceleration: float = rot_acceleration
        """The rotational acceleration of the particle."""
        self.scale: float = scale
        """The scale of the particle."""
        self.lifespan: float = lifespan
        """The lifespan of the particle. (in seconds)"""
        self.z_index: int = z_index
        """The z index of the particle."""
        self.age: float = age
        """The age of the particle. (in seconds)"""
        self._original_scale: Vector = self.surface.scale.clone()
        self._system_pos: Vector = Vector()
        self._system_rotation: float = 0
        self._system_z: int = 0

    @staticmethod
    def default_movement(particle: Particle, dt: float):
        """The default movement function."""
        particle.velocity += particle.acceleration * dt
        particle.pos += particle.velocity * dt

        particle.rot_velocity += particle.rot_acceleration * dt
        particle.rotation += particle.rot_velocity * dt
