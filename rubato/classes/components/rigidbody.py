"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from __future__ import annotations
import math

from . import Component, Circle, Hitbox, Rectangle, Polygon
from ... import Vector, Time, Math


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.
    Rigidbodies require hitboxes.

    Args:
        offset: The offset of the rigidbody from the gameobject. Defaults to Vector(0, 0).
        rot_offset: The offset of the rigidbody's rotation from the gameobject. Defaults to 0.
        density: The density of the rigidbody. Defaults to 1.
        bounciness: The bounciness of the rigidbody. Defaults to 0.
        gravity: The gravity of the rigidbody. Defaults to Vector(0, 0).
        max_speed: The maximum speed of the rigidbody. Defaults to Vector(INF, INF).
        velocity: The velocity of the rigidbody. Defaults to Vector(0, 0).
        ang_vel: The angular velocity of the rigidbody. Defaults to 0.
        friction: The friction of the rigidbody. Defaults to 0.
        static: Whether the rigidbody is static. Defaults to False.
        pos_correction: The positional correction of the rigidbody. Defaults to 0.25.
        moment: The moment of inertia of the rigidbody. Defaults to -1.
        mass: The mass of the rigidbody. Defaults to -1.
        advanced: Whether the rigidbody uses advanced physics. Defaults to False.

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
        ang_vel (float): The current angular velocity of the Rigidbody.
        bounciness (float): How bouncy the rigidbody is (usually a value
            between 0 and 1).
        advanced (bool): Whether to use rotational collision resolution
            (not desired in basic platformers, for instance).
    """

    def __init__(
        self,
        offset: Vector = Vector(),
        rot_offset: float = 0,
        density: float = 1,
        bounciness: float = 0,
        gravity: Vector = Vector(),
        max_speed: Vector = Vector(Math.INF, Math.INF),
        velocity: Vector = Vector(),
        ang_vel: float = 0,
        friction: float = 0,
        static: bool = False,
        pos_correction: float = 0.25,
        moment: float = -1,
        mass: float = -1,
        advanced: bool = False,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset)

        self.static: bool = static

        self.gravity: Vector = gravity
        self.friction: float = friction
        self.max_speed: Vector = max_speed

        self.pos_correction: float = pos_correction
        self.advanced: bool = advanced

        self.velocity: Vector = velocity
        self.ang_vel: float = ang_vel

        self.singular = True

        if mass != -1 and moment != -1:
            if mass == 0 or self.static:
                self._inv_mass = 0
            else:
                self._inv_mass: float = 1 / mass

            if moment == 0 or self.static:
                self._inv_moment = 0
            else:
                self._inv_moment: float = 1 / moment
            self._density = -1
        else:
            self._density = density
            self._inv_mass = 0
            self._inv_moment = 0

        self._last_density_calc = -1
        self.bounciness: float = bounciness

    @property
    def inv_mass(self) -> float:
        """The inverse mass of the Rigidbody."""
        self.calc_mass_and_moment()
        return self._inv_mass

    @inv_mass.setter
    def inv_mass(self, new: float):
        self._inv_mass = new

    @property
    def mass(self) -> float:
        """The mass of the Rigidbody."""
        self.calc_mass_and_moment()
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
    def inv_moment(self) -> float:
        """The inverse moment of the Rigidbody."""
        self.calc_mass_and_moment()
        return self._inv_moment

    @inv_moment.setter
    def inv_moment(self, new: float):
        self._inv_moment = new

    @property
    def moment(self) -> float:
        """The moment of inertia of the Rigidbody."""
        self.calc_mass_and_moment()
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

    def calc_mass_and_moment(self):
        """
        Calculates the mass and the moment of interia from the density if it hasn't already been calculate this frame.
        """
        if self._density > -1 and self._last_density_calc < Time.frames:
            self._last_density_calc = Time.frames
            hitboxes = self.gameobj.get_all(Hitbox)
            tots_mass = 0
            tots_moment = 0
            for hitbox in hitboxes:
                if hitbox.trigger:
                    continue
                if isinstance(hitbox, Circle):
                    mass = self._density * hitbox.radius**2 * math.pi
                    moment = mass * hitbox.radius**2
                elif isinstance(hitbox, Rectangle):
                    mass = self._density * hitbox.width * hitbox.height
                    moment = mass * (hitbox.width**2 + hitbox.height**2) / 12
                elif isinstance(hitbox, Polygon):
                    c = Vector(0, 0)  # centroid
                    area = 0
                    inert = 0
                    k_inv3 = 1 / 3

                    verts = hitbox.translated_verts()
                    for i in range(len(verts)):
                        p1 = verts[i]
                        p2 = verts[(i + 1) % len(verts)]

                        d = p1.cross(p2)
                        tri_area = 0.5 * d

                        area += tri_area

                        # Use area to weight the centroid average, not just vertex position
                        weight = tri_area * k_inv3
                        c += (p1 + p2) * weight

                        intx2 = p1.x**2 + p2.x * p1.x + p2.x**2
                        inty2 = p1.y**2 + p2.y * p1.y + p2.y**2
                        inert += (0.25 * k_inv3 * d) * (intx2 + inty2)

                    mass = self._density * area
                    moment = inert * self._density

                tots_mass += mass
                tots_moment += moment

            self._inv_mass = 0 if tots_mass == 0 else 1 / tots_mass
            self._inv_moment = 0 if tots_moment == 0 else 1 / tots_moment

    def physics(self):
        """Applies general kinematic laws to the rigidbody."""
        self.velocity += self.gravity * Time.milli_to_sec(Time.fixed_delta)
        self.velocity.clamp(-self.max_speed, self.max_speed)

        self.gameobj.pos += self.velocity * Time.milli_to_sec(Time.fixed_delta)
        self.gameobj.rotation += self.ang_vel * Time.milli_to_sec(Time.fixed_delta)

    def add_force(self, force: Vector):
        """
        Applies a force to the Rigidbody.

        Args:
            force (Vector): The force to add.
        """
        accel = force * self.inv_mass

        self.velocity += accel * Time.milli_to_sec(Time.fixed_delta)

    def add_impulse(self, impulse: Vector):
        """
        Applies an impulse to the rigidbody.

        Args:
            impulse (Vector): _description_
        """
        self.velocity += impulse * Time.milli_to_sec(Time.fixed_delta)

    def add_cont_force(self, force: Vector, time: int):
        """
        Add a continuous force to the Rigidbody.
        A continuous force is a force that is continuously applied over a time period.
        (the force is added every frame for a specific duration).

        Args:
            force (Vector): The force to add.
            time (int): The time in seconds that the force should be added.
        """
        if time <= 0:
            return
        else:
            self.add_force(force)
            Time.delayed_frames(1, lambda: self.add_cont_force(force, time - Time.delta_time))

    def add_cont_impulse(self, impulse: Vector, time: int):
        """
        Add a continuous impulse to the Rigidbody.
        A continuous impulse is a impulse that is continuously applied over a time period.
        (the impulse is added every frame for a specific duration).

        Args:
            impulse (Vector): The impulse to add.
            time (int): The time in seconds that the impulse should be added.
        """
        if time <= 0:
            return
        else:
            self.add_impulse(impulse)
            Time.delayed_frames(1, lambda: self.add_cont_impulse(impulse, time - Time.delta_time))

    def setup(self):
        self.calc_mass_and_moment()

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
