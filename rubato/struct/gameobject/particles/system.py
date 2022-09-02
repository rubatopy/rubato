"""A simple particle system."""
from __future__ import annotations
from enum import IntEnum, unique
from random import randint
from typing import Callable
import cython

from . import Particle
from .. import Component
from ... import Surface
from .... import Vector, Camera, Time, Math, Color, Draw

if not cython.compiled:
    from enum_tools import document_enum
else:
    document_enum = lambda _: None


@unique
class ParticleSystemMode(IntEnum):
    """
    The mode of the particle system.
    """
    RANDOM = 0
    """The particles are generated randomly."""
    LOOP = 1
    """Animate the generation around the shape."""
    PINGPONG = 2
    """Animate the generation in a pingpong fashion."""
    BURST = 3
    """Generate the particles in a burst."""


if not cython.compiled:
    document_enum(ParticleSystemMode)


class ParticleSystem(Component):
    """
    A simple particle system.

    Args:
        new_particle: The method to generate a new particle. Should return a particle object.
            Defaults to `ParticleSystem.default_particle`.
        duration: The duration of the system in seconds (when to stop generating particles). Defaults to 5.
        loop: Whether the system should loop (start again at the end of its duration). Defaults to False.
        max_particles: The maximum number of particles in the system. Defaults to `Math.INF`.
        mode: The particle generation mode of the system. Defaults to `ParticleSystemMode.RANDOM`.
        spread: The gap between particles (in degrees). Defaults to 45.
        density: The density of the system. This is the number of particles generated per fixed update. Defaults to 1.
        local_space: Whether the particles should be in local space.
        offset: The offset of the system. Defaults to (0, 0).
        rot_offset: The rotation offset of the system. Defaults to 0.
        z_index: The z-index of the system. Defaults to 0.
    """

    def __init__(
        self,
        new_particle: Callable[[float], Particle] | None = None,
        duration: float = 5,
        loop: bool = False,
        max_particles: int = Math.INF,
        mode: ParticleSystemMode = ParticleSystemMode.RANDOM,
        spread: float = 5,
        density: int = 1,
        local_space: bool = False,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)
        self.new_particle = new_particle or ParticleSystem.default_particle
        """The user-defined function that generates a particle."""
        self.duration: float = duration
        """The duration of the system in seconds."""
        self.loop: bool = loop
        """Whether the system should loop."""
        self.max_particles: int = max_particles
        """The maximum number of particles in the system."""
        self.mode: ParticleSystemMode = mode
        """The particle generation mode of the system."""
        self.spread: float = spread
        """The gap between particles (in degrees)."""
        self.density: int = density
        """The density of the system. This is the number of particles generated per fixed update."""
        self.local_space: bool = local_space
        """Whether the particles should be in local space."""

        self.__particles: list[Particle] = []
        self.__running: bool = False
        self.__time: float = 0
        self.__generated: int = 0
        """
        Number of particles generated this loop. (NOT EQUAL TO TOTAL NUMBER OF PARTICLES)
        """
        self.__forward: bool = True
        """This controls the direction of the particle generation. (Only used in ParticleSystemMode.PINGPONG)"""

    def num_particles(self):
        """
        The number of particles in the system.
        """
        return len(self.__particles)

    def start(self):
        """Start the system."""
        self.__running = True

    def stop(self):
        """Stop the system."""
        self.__running = False

    def fixed_update(self):
        if self.__running:
            self.generate_particles()
            self.__time += Time.fixed_delta
            if self.__time >= self.duration:
                if self.loop:
                    self.__time = 0
                    self.__generated = 0
                    self.__forward = not self.__forward
                else:
                    self.__running = False

        i: int = 0
        while i < len(self.__particles):
            particle = self.__particles[i]
            if particle.age >= particle.lifespan:
                self.__particles.pop(i)
            else:
                particle.age += Time.fixed_delta
                particle.movement(particle, Time.fixed_delta)
                i += 1

    def draw(self, camera: Camera):
        for particle in self.__particles:
            if self.local_space:
                particle._system_z = self.true_z()
                particle._system_pos = self.true_pos().clone()
                particle._system_rotation = self.true_rotation()

            particle.surface.rotation = particle.rotation + particle._system_rotation
            particle.surface.scale = particle._original_scale * particle.scale
            Draw.queue_surface(
                particle.surface,
                particle._system_pos + particle.pos.rotate(particle._system_rotation),
                particle.z_index + particle._system_z,
                camera,
            )

    def generate_particles(self):
        """
        Generates particles. Called automatically by fixed_update.
        """
        max_in_dur = round(360 / self.spread) * self.density
        for _ in range(self.density):
            if self.mode == ParticleSystemMode.BURST and self.__time == 0:
                while self.__generated < max_in_dur and len(self.__particles) < self.max_particles:
                    self.gen_particle(self.__generated * self.spread)
            if len(self.__particles) < self.max_particles:
                if self.mode == ParticleSystemMode.RANDOM:
                    self.gen_particle(randint(0, max_in_dur) * self.spread)
                elif self.__time >= self.duration / max_in_dur * self.__generated:
                    if self.mode == ParticleSystemMode.LOOP:
                        self.gen_particle(self.__generated * self.spread)
                    elif self.mode == ParticleSystemMode.PINGPONG:
                        if self.__forward:
                            self.gen_particle(self.__generated * self.spread)
                        else:
                            self.gen_particle((max_in_dur - self.__generated) * self.spread)

    def gen_particle(self, angle: float):
        part = self.new_particle(angle)
        if not self.local_space:
            part._system_rotation = self.true_rotation()
            part._system_pos = self.true_pos().clone()
            part._system_z = self.true_z()
        self.__particles.append(part)
        self.__generated += 1

    def clear(self):
        """Clear the system."""
        self.__particles.clear()

    def clone(self) -> ParticleSystem:
        return ParticleSystem(
            self.new_particle,
            self.duration,
            self.loop,
            self.max_particles,
            self.mode,
            self.spread,
            self.density,
            self.local_space,
            self.offset.clone(),
            self.rot_offset,
            self.z_index,
        )

    @classmethod
    def default_particle(cls, angle: float) -> Particle:
        surf = Surface()
        surf.fill(Color.debug)
        return Particle(surf, velocity=cls.circle_direction()(angle))

    @staticmethod
    def circle_shape(radius: float) -> Callable[[float], Vector]:
        """
        A shape function that returns a circle. This can be passed into the starting_shape argument of a ParticleSystem.

        Args:
            radius: The radius of the circle.
        """

        def shape(angle: float) -> Vector:
            return Vector.from_radial(radius, angle)

        return shape

    @staticmethod
    def circle_direction() -> Callable[[float], Vector]:
        """
        A direction function that returns a circle. This can be passed into the starting_dir argument of a
        ParticleSystem.
        """

        def direction(angle: float) -> Vector:
            return Vector.from_radial(1, angle)

        return direction

    @staticmethod
    def square_shape(size: float) -> Callable[[float], Vector]:
        """
        A shape function that returns a square. This can be passed into the starting_shape argument of a ParticleSystem.

        Args:
            size: The size of the square.
        """

        def shape(angle: float) -> Vector:
            angle %= 360
            if 0 <= angle < 90:
                return Vector(((angle / 45) - 1) * size, -size / 2)
            elif 90 <= angle < 180:
                return Vector(size / 2, (((angle - 90) / 45) - 1) * size)
            elif 180 <= angle < 270:
                return Vector((((angle - 180) / 45) - 1) * size, size / 2)
            else:
                return Vector(-size / 2, (((angle - 270) / 45) - 1) * size)

        return shape

    @staticmethod
    def square_direction() -> Callable[[float], Vector]:
        """
        A direction function that returns a square. This can be passed into the starting_dir argument of a
        ParticleSystem.
        """

        def direction(angle: float) -> Vector:
            angle %= 360
            if 0 <= angle < 90:
                return Vector(0, -1)
            elif 90 <= angle < 180:
                return Vector(1, 0)
            elif 180 <= angle < 270:
                return Vector(0, 1)
            else:
                return Vector(-1, 0)

        return direction
