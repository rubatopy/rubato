"""A simple particle system."""
from dataclasses import dataclass
from typing import Callable
from . import Particle


@dataclass(frozen=True, slots=True)
class ParticleSystemConfig:
    """Configuration for a particle system."""
    lifespan: float
    start_speed: float
    start_rotation: float
    start_scale: float
    duration: float
    loop: bool


class ParticleSystem:
    pass
