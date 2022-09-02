"""
The Rigidbody component describes how the physics engine handles a game object.
"""
from __future__ import annotations

from .. import Component
from .... import Vector, Time, Math


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.
    Rigidbodies require hitboxes.

    Args:
        mass: The mass of the rigidbody. Defaults to -1.
        gravity: The gravity of the rigidbody. Defaults to (0, 0).
        friction: The friction of the rigidbody. Defaults to 0.
        static: Whether the rigidbody is static. Defaults to False.
        bounciness: The bounciness of the rigidbody. Defaults to 0.
        max_speed: The maximum speed of the rigidbody. Defaults to (INF, INF).
        velocity: The velocity of the rigidbody. Defaults to (0, 0).
        ang_vel: The angular velocity of the rigidbody. Defaults to 0.
        pos_correction: The positional correction of the rigidbody. Defaults to 0.25.
        offset: The offset of the rigidbody from the gameobject. Defaults to (0, 0).
        rot_offset: The offset of the rigidbody's rotation from the gameobject. Defaults to 0.
        z_index: The z-index of the rigidbody. Defaults to 0.
    """

    def __init__(
        self,
        mass: float = 1,
        gravity: Vector | tuple[float, float] = (0, 0),
        friction: float = 0,
        static: bool = False,
        bounciness: float = 0,
        max_speed: Vector | tuple[float, float] = (Math.INF, Math.INF),
        velocity: Vector | tuple[float, float] = (0, 0),
        ang_vel: float = 0,
        pos_correction: float = 0.25,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index)

        self.static: bool = static
        """Whether the rigidbody is static (as in, it does not move)."""

        self.gravity: Vector = Vector.create(gravity)
        """The acceleration of the gravity that should be applied."""
        self.friction: float = friction
        """The friction coefficient of the Rigidbody (usually a value between 0 and 1)."""
        self.max_speed: Vector = Vector.create(max_speed)
        """The maximum speed of the Rigidbody."""

        self.pos_correction: float = pos_correction
        """The positional correction of the rigidbody."""

        self.velocity: Vector = Vector.create(velocity)
        """The current velocity of the Rigidbody."""
        self.ang_vel: float = ang_vel
        """The current angular velocity of the Rigidbody."""

        self.singular: bool = True

        if mass == 0 or self.static:
            self.inv_mass: float = 0
            """The inverse mass of the Rigidbody."""
        else:
            self.inv_mass: float = 1 / mass

        self.bounciness: float = bounciness
        """How bouncy the rigidbody is (usually a value between 0 and 1)."""

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

    def physics(self):
        """Applies general kinematic laws to the rigidbody."""
        self.velocity += self.gravity * Time.fixed_delta
        self.velocity.clamp(-self.max_speed, self.max_speed)  # pylint: disable=invalid-unary-operand-type

        self.gameobj.pos += self.velocity * Time.fixed_delta
        self.gameobj.rotation += self.ang_vel * Time.fixed_delta

    def add_force(self, force: Vector | tuple[float, float]):
        """
        Applies a force to the Rigidbody.

        Args:
            force: The force to add.
        """
        self.velocity.x += force[0] * self.inv_mass * Time.fixed_delta
        self.velocity.y += force[1] * self.inv_mass * Time.fixed_delta

    def add_impulse(self, impulse: Vector | tuple[float, float]):
        """
        Applies an impulse to the rigidbody.

        Args:
            impulse: The impulse to add.
        """
        self.velocity.x += impulse[0] * Time.fixed_delta
        self.velocity.y += impulse[1] * Time.fixed_delta

    def add_cont_force(self, force: Vector | tuple[float, float], time: float):
        """
        Add a continuous force to the Rigidbody.
        A continuous force is a force that is continuously applied over a time period.
        (the force is added every frame for a specific duration).

        Args:
            force: The force to add.
            time: The time in seconds that the force should be added.
        """
        if time <= 0:
            return
        else:
            self.add_force(force)
            Time.next_frame(lambda: self.add_cont_force(force, time - Time.delta_time))

    def add_cont_impulse(self, impulse: Vector | tuple[float, float], time: float):
        """
        Add a continuous impulse to the Rigidbody.
        A continuous impulse is a impulse that is continuously applied over a time period.
        (the impulse is added every frame for a specific duration).

        Args:
            impulse: The impulse to add.
            time: The time in seconds that the impulse should be added.
        """
        if time <= 0:
            return
        else:
            self.add_impulse(impulse)
            Time.next_frame(lambda: self.add_cont_impulse(impulse, time - Time.delta_time))

    def fixed_update(self):
        """The physics loop for the rigidbody component."""
        if not self.static:
            self.physics()

    def clone(self) -> RigidBody:
        return RigidBody(
            mass=self.mass,
            gravity=self.gravity.clone(),
            friction=self.friction,
            static=self.static,
            bounciness=self.bounciness,
            max_speed=self.max_speed.clone(),
            velocity=self.velocity.clone(),
            ang_vel=self.ang_vel,
            pos_correction=self.pos_correction,
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            z_index=self.z_index
        )
