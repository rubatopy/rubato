"""A simple particle system."""
from typing import Callable, Literal

from rubato.utils.rb_math import Math
from . import Particle
from .. import Component
from ... import Surface
from .... import Vector, Camera, Time


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
        mode: The particle generation mode of the system. Defaults to "random".
            random - The particles are generated randomly.
            loop - Animate the generation around the shape.
            pingpong - Animate the generation in a pingpong fashion.
            burst - Generate the particles in a burst.
        spread: The spread of the system. This is the number of particles generated per loop. Defaults to 5.
        movement: The movement function of a particle. Defaults to `ParticleSystem.default_movement`
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
        mode: Literal["random", "loop", "pingpong", "burst"] = "random",
        spread: int = 5,
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
        self.mode: Literal["random", "loop", "pingpong", "burst"] = mode
        """
        The particle generation mode of the system.
        
        random - The particles are generated randomly.

        loop - Animate the generation around the shape.

        pingpong - Animate the generation in a pingpong fashion.

        burst - Generate the particles in a burst.
        """
        self.spread: int = spread
        """The spread of the system. This is the number of particles generated per loop."""

        if movement is None:
            self.movement: Callable[[Particle, float], None] = ParticleSystem.default_movement
            """The movement function of a particle."""
        else:
            self.movement: Callable[[Particle, float], None] = movement

        self.__particles: list[Particle] = []
        self.__running: bool = False
        self.__time: float = duration

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
        i = 0
        while i < len(self.__particles):
            if self.__particles[i].age >= self.__particles[i].lifespan:
                self.__particles.pop(i)
            else:
                self.__particles[i]._fixed_update()
            i += 1

        if self.__running:
            self.__time += Time.fixed_delta
            if self.__time >= self.duration:
                self.generate_particles()
                if self.loop:
                    self.__time = 0
                else:
                    self.__running = False

    def draw(self, camera: Camera):
        for particle in self.__particles:
            particle._draw(camera)

    def generate_particles(self):
        """
        Generates particles.
        """
        generated = 0

        while generated < self.spread and len(self.__particles) < self.max_particles:
            angle = generated * (360 / self.spread)
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
            generated += 1

    @staticmethod
    def default_movement(particle: Particle, delta: float):
        """
        The default movement function of a particle.

        Args:
            particle: The particle to move.
            delta: The time delta.
        """
        particle.pos += particle.velocity * delta
