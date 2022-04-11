"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from __future__ import annotations

from . import Component
from ... import Vector, Defaults, Time


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.
    Rigidbodies require hitboxes.

    Attributes:
        static (bool): Whether or not the rigidbody is static (as in, it does
            not move).
        gravity (Vector): The acceleration of the gravity that should be
            applied.
        friction (float): The friction coefficient of the Rigidbody (usually a
            a value between 0 and 1).
        max_speed (Vector): The maximum speed of the Rigidbody.
        min_speed (Vector): The minimum speed of the Rigidbody.
        velocity (Vector): The current velocity of the Rigidbody.
        inv_mass (float): The inverse of the mass of the Rigidbody (0 if the
            mass is infinite).
        bounciness (float): How bouncy the rigidbody is (usually a value
            between 0 and 1).
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Rigidbody.

        Args:
            options: A rigidbody config. Defaults to the :ref:`Rigidbody defaults <rigidbodydef>`.
        """
        params = Defaults.rigidbody_defaults | options

        super().__init__()

        self.static: bool = params["static"]

        self.gravity: Vector = params["gravity"]
        self.friction: float = params["friction"]
        self.max_speed: Vector = params["max_speed"]

        self.pos_correction: float = params["pos_correction"]

        self.velocity: Vector = params["velocity"]
        self.ang_vel: float = params["ang_vel"]

        self.singular = True

        if params["mass"] == 0 or self.static:
            self.inv_mass = 0
        else:
            self.inv_mass: float = 1 / params["mass"]

        if params["moment"] == 0 or self.static:
            self.inv_moment = 0
        else:
            self.inv_moment: float = 1 / params["moment"]

        self.bounciness: float = params["bounciness"]

    @property
    def mass(self) -> float:
        """The mass of the Rigidbody."""
        if self.inv_mass == 0:
            return 0
        else:
            return 1 / self.inv_mass

    @mass.setter
    def mass(self, new: float):
        if new == 0:
            self.inv_mass = 0
        else:
            self.inv_mass: float = 1 / new

    @property
    def moment(self) -> float:
        """The moment of inertia of the Rigidbody."""
        if self.inv_moment == 0:
            return 0
        else:
            return 1 / self.inv_moment

    @moment.setter
    def moment(self, new: float):
        if new == 0:
            self.inv_moment = 0
        else:
            self.inv_moment: float = 1 / new

    def physics(self):
        """Applies general kinematic laws to the rigidbody."""
        self.add_force(self.gravity * self.mass)

        self.velocity.clamp(-self.max_speed, self.max_speed)

        self.gameobj.pos += self.velocity * Time.milli_to_sec(Time.fixed_delta)
        self.gameobj.rotation += self.ang_vel * Time.milli_to_sec(Time.fixed_delta)

    def add_force(self, force: Vector):
        """
        Add a force to the Rigidbody.

        Args:
            force (Vector): The force to add.
        """
        accel = force * self.inv_mass

        self.velocity += accel * Time.milli_to_sec(Time.fixed_delta)

    def add_cont_force(self, impulse: Vector, time: int):
        """
        Add a continuous force to the Rigidbody.
        A continuous force is a force that is continuously applied over a time period.
        (the force is added every frame for a specific duration).

        Args:
            impulse (Vector): The force to add.
            time (int): The time in seconds that the force should be added.
        """
        if time <= 0:
            return
        else:
            self.add_force(impulse)
            Time.delayed_frames(1, lambda: self.add_impulse(impulse, time - Time.delta_time))

    def fixed_update(self):
        """The physics loop for the rigidbody component."""
        if not self.static:
            self.physics()

    def clone(self) -> RigidBody:
        return RigidBody(
            {
                "static": self.static,
                "gravity": self.gravity,
                "friction": self.friction,
                "max_speed": self.max_speed,
                "pos_correction": self.pos_correction,
                "velocity": self.velocity,
                "mass": self.mass,
                "bounciness": self.bounciness,
            }
        )
