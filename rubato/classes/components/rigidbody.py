"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from . import Component
from ... import Vector, Defaults, Time

if TYPE_CHECKING:
    from . import Manifold


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

        self.singular = True

        if params["mass"] == 0 or self.static:
            self.inv_mass = 0
        else:
            self.inv_mass: float = 1 / params["mass"]

        self.bounciness: float = params["bounciness"]

    @property
    def mass(self) -> float:
        """The mass of the Rigidbody (readonly)"""
        if self.inv_mass == 0:
            return 0
        else:
            return 1 / self.inv_mass

    def physics(self):
        """Applies general kinematic laws to the rigidbody."""
        self.add_force(self.gravity * self.mass)

        self.velocity.clamp(-self.max_speed, self.max_speed)

        self.gameobj.pos += self.velocity * Time.milli_to_sec(Time.fixed_delta)

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

    @staticmethod
    def handle_collision(col: Manifold):
        """
        Resolve the collision between two rigidbodies.
        Utilizes a simplistic impulse resolution method.

        Args:
            col: The collision information.
        """
        # Get the rigidbody components
        rb_a: RigidBody = col.shape_b.gameobj.get(RigidBody)
        rb_b: RigidBody = col.shape_a.gameobj.get(RigidBody)

        rb_a_none = rb_a is None
        rb_b_none = rb_b is None

        if rb_a_none and rb_b_none:
            return

        # Find inverse masses
        inv_mass_a: float = 0 if rb_a_none else rb_a.inv_mass
        inv_mass_b: float = 0 if rb_b_none else rb_b.inv_mass

        # Handle infinite mass cases
        if inv_mass_a == inv_mass_b == 0:
            if rb_a_none:
                inv_mass_b = 1
            elif rb_b_none:
                inv_mass_a = 1
            else:
                inv_mass_a, inv_mass_b = 1, 1

        inv_sys_mass = 1 / (inv_mass_a + inv_mass_b)

        # Find collision separation normal
        collision_norm = col.sep.unit()

        # Position correction
        correction = max(col.sep.magnitude - 0.01, 0) * inv_sys_mass * collision_norm

        # Impulse Resolution

        # Relative velocity
        rv = (0 if rb_b_none else rb_b.velocity) - (0 if rb_a_none else rb_a.velocity)

        if (vel_along_norm := rv.dot(collision_norm)) > 0:
            return

        # Calculate restitution
        e = max(0 if rb_a_none else rb_a.bounciness, 0 if rb_b_none else rb_b.bounciness)

        # Calculate impulse scalar
        j = -(1 + e) * vel_along_norm * inv_sys_mass

        # Apply the impulse
        impulse = j * collision_norm

        if not (rb_a_none or rb_a.static):
            rb_a.gameobj.pos -= inv_mass_a * correction * rb_a.pos_correction
            rb_a.velocity -= inv_mass_a * impulse

        if not (rb_b_none or rb_b.static):
            rb_b.gameobj.pos += inv_mass_b * correction * rb_b.pos_correction
            rb_b.velocity += inv_mass_b * impulse

        # Friction

        # Calculate friction coefficient
        if rb_a_none:
            mu = rb_b.friction * rb_b.friction
        elif rb_b_none:
            mu = rb_a.friction * rb_a.friction
        else:
            mu = min(rb_a.friction * rb_a.friction, rb_b.friction * rb_b.friction)

        # Stop redundant friction calculations
        if mu == 0:
            return

        # Tangent vector
        tangent = rv - rv.dot(collision_norm) * collision_norm
        tangent.magnitude = 1

        # Solve for magnitude to apply along the friction vector
        jt = -rv.dot(tangent) * inv_sys_mass

        # Calculate friction impulse
        if abs(jt) < j * mu:
            friction_impulse = jt * tangent  # "Static friction"
        else:
            friction_impulse = -j * tangent * mu  # "Dynamic friction"

        if not (rb_a_none or rb_a.static):
            rb_a.velocity -= inv_mass_a * friction_impulse

        if not (rb_b_none or rb_b.static):
            rb_b.velocity += inv_mass_b * friction_impulse
