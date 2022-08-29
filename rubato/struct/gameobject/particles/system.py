"""A simple particle system."""
from __future__ import annotations
from enum import IntEnum, unique
from random import choice
from typing import Callable
import cython

from . import Particle
from .. import Component
from ... import Surface
from .... import Vector, Camera, Time, Math

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
        surface: The surface to use for each particle.
        lifespan: The lifespan of a particle in second. Defaults to 5.
        start_speed: The starting speed of a particle. Defaults to 5.
        start_rotation: The starting rotation of a particle. Defaults to 0.
        start_scale: The starting scale of a particle. Defaults to 1.
        duration: The duration of the system in seconds. Defaults to 5.
        loop: Whether the system should loop. Defaults to False.
        max_particles: The maximum number of particles in the system. Defaults to Math.INF.
        starting_shape: The starting shape function of the system. If an int is given, the shape is a circle with the
            given radius. Defaults to 1.
        starting_dir: The starting direction function of the system. If None, the direction is away from the center.
            Defaults to None.
        mode: The particle generation mode of the system. Defaults to ParticleSystemMode.RANDOM.
        spread: The spread of the system. This is the number of particles generated per loop. Defaults to 5.
        density: The density of the system. This is the number of particles generated per fixed update. Defaults to 1.
        movement: The movement function of a particle. Defaults to `ParticleSystem.default_movement`.
        offset: The offset of the system. Defaults to (0, 0).
        rot_offset: The rotation offset of the system. Defaults to 0.
        z_index: The z-index of the system. Defaults to 0.
    """

    def __init__(
        self,
        surface: Surface,
        lifespan: float = 5,
        start_speed: float = 5,
        start_rotation: float = 0,
        start_scale: float = 1,
        duration: float = 5,
        loop: bool = False,
        max_particles: int = Math.INF,
        starting_shape: Callable[[float], Vector] | int = 1,
        starting_dir: Callable[[float], Vector] | None = None,
        mode: ParticleSystemMode = ParticleSystemMode.RANDOM,
        spread: int = 5,
        density: int = 1,
        movement: Callable[[Particle, float], None] | None = None,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)
        self.surface = surface
        """The surface of each particle."""
        self.lifespan: float = lifespan
        """The lifespan of a particle in seconds."""
        self.start_speed: float = start_speed
        """The starting speed of a particle."""
        self.start_rotation: float = start_rotation
        """The starting rotation of a particle."""
        self.start_scale: float = start_scale
        """The starting scale of a particle."""
        self.duration: float = duration
        """The duration of the system in seconds."""
        self.loop: bool = loop
        """Whether the system should loop."""
        self.max_particles: int = max_particles
        """The maximum number of particles in the system."""
        if isinstance(starting_shape, int):
            self.starting_shape: Callable[[float], Vector] = lambda a: Vector.from_radial(
                starting_shape,
                a,
            )
            """The starting shape function of the system."""
        else:
            self.starting_shape: Callable[[float], Vector] = starting_shape
        if starting_dir is None:
            self.starting_dir: Callable[[float], Vector] = lambda a: Vector.from_radial(
                1,
                a,
            )
            """The starting direction function of the system."""
        else:
            self.starting_dir: Callable[[float], Vector] = starting_dir
        self.mode: ParticleSystemMode = mode
        """The particle generation mode of the system."""
        self.spread: int = spread
        """The spread of the system. This is the number of particles generated per loop."""
        self.density: int = density
        """The density of the system. This is the number of particles generated per fixed update."""

        if movement is None:
            self.movement: Callable[[Particle, float], None] = ParticleSystem.default_movement
            """The movement function of a particle."""
        else:
            self.movement: Callable[[Particle, float], None] = movement

        self.__particles: list[Particle] = []
        self.__running: bool = False
        self.__time: float = duration
        self.__generated: int = 0
        """
        Number of particles generated this loop. (NOT EQUAL TO TOTAL NUMBER OF PARTICLES)
        If mode is RANDOM, then each bit corresponds to a generated particle this loop.
        """
        self.__forward: bool = True
        """This controls the direction of the particle generation. (Only used in ParticleSystemMode.PINGPONG)"""

    @property
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

        i = 0
        while i < len(self.__particles):
            if self.__particles[i].age >= self.__particles[i].lifespan:
                self.__particles.pop(i)
            else:
                self.__particles[i].fixed_update()
            i += 1

    def draw(self, camera: Camera):
        for particle in self.__particles:
            particle.draw(camera)

    def generate_particles(self):
        """
        Generates particles. Called automatically by fixed_update.
        """
        for _ in range(self.density):
            if self.mode == ParticleSystemMode.BURST and self.__time == 0:
                while self.__generated < self.spread and len(self.__particles) < self.max_particles:
                    self.new_particle(self.__generated)
                    self.__generated += 1
            elif self.mode == ParticleSystemMode.RANDOM:
                gened = [bool(self.__generated & 1 << n) for n in range(self.spread)]
                if available := [i for i, x in enumerate(gened) if not x]:
                    i = choice(available)
                    self.new_particle(i)
                    self.__generated |= 1 << i
            elif self.__generated < self.spread and len(
                self.__particles
            ) < self.max_particles and self.__time >= self.duration / self.spread * self.__generated:
                if self.mode == ParticleSystemMode.LOOP:
                    self.new_particle(self.__generated)
                    self.__generated += 1
                elif self.mode == ParticleSystemMode.PINGPONG:
                    if self.__forward:
                        self.new_particle(self.__generated)
                    else:
                        self.new_particle(self.spread - self.__generated)
                    self.__generated += 1

    def new_particle(self, i: int):
        """
        Generate a new particle and add it to the system.

        Args:
            i: The generation index of the particle.
        """
        angle = i * (360 / self.spread)
        self.__particles.append(
            Particle(
                self.movement,
                self.starting_dir(angle).rotate(self.true_rotation()) * self.start_speed,
                self.starting_shape(angle).rotate(self.true_rotation()) + self.true_pos(),
                self.start_rotation,
                self.start_scale,
                self.surface.clone(),
                self.lifespan,
                self.z_index,
            )
        )

    def clone(self) -> ParticleSystem:
        return ParticleSystem(
            self.surface.clone(),
            self.lifespan,
            self.start_speed,
            self.start_rotation,
            self.start_scale,
            self.duration,
            self.loop,
            self.max_particles,
            self.starting_shape,
            self.starting_dir,
            self.mode,
            self.spread,
            self.density,
            self.movement,
            self.offset.clone(),
            self.rot_offset,
            self.z_index,
        )

    def delete(self):
        self.surface.delete()
        for particle in self.__particles:
            particle.delete()
        self.__particles.clear()

    @staticmethod
    def default_movement(particle: Particle, delta: float):
        """
        The default movement function of a particle.

        Args:
            particle: The particle to move.
            delta: The time delta.
        """
        particle.pos += particle.velocity * delta
