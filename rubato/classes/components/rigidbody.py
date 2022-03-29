"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from typing import TYPE_CHECKING
from rubato.classes.component import Component
from rubato.utils import Vector, Defaults, Time

if TYPE_CHECKING:
    from rubato.classes.components.hitbox import ColInfo


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
            options: A rigidbody config. Defaults to the |default| for
                `RigidBody`
        """
        params = Defaults.rigidbody_defaults | options

        super().__init__()

        self.static: bool = params["static"]

        self.gravity: Vector = params["gravity"]
        self.friction: float = params["friction"]
        self.max_speed: Vector = params["max_speed"]

        self.velocity: Vector = params["velocity"]

        self.singular = True

        # self.angvel: float = 0
        # self.rotation: float = params["rotation"]

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
        """The physics calculation"""
        # Apply gravity
        self.add_force(self.gravity * self.mass)

        self.velocity.clamp(-self.max_speed, self.max_speed)

        self.gameobj.pos += self.velocity * Time.milli_to_sec(Time.fixed_delta)

    def add_force(self, force: Vector):
        """
        Add a force to the Rigidbody.

        Args:
            force: The force to add.
        """
        accel = force * self.inv_mass

        self.velocity += accel * Time.milli_to_sec(Time.fixed_delta)

    def add_cont_force(self, impulse: Vector, time: int):
        """
        Add a continuous force to the Rigidbody. A continuous force is a force
        that is continuously applied over a time period. (the force is added
        every frame for a specific duration).

        Args:
            impulse: The force to add.
            time: The time in seconds that the force should be added.
        """
        if time <= 0:
            return
        else:
            self.add_force(impulse)

            Time.delayed_frames(1, lambda: self.add_impulse(impulse, time - Time.delta_time))

    @staticmethod
    def handle_collision(col: "ColInfo"):
        """
        Handle the collision between two rigidbodies.

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

        sep_mag = (col.sep.x * col.sep.x + col.sep.y * col.sep.y)**.5

        # Find collision separation normal
        collision_norm_x, collision_norm_y = col.sep.x / sep_mag, col.sep.y / sep_mag

        # Position correction
        multiplier = max(sep_mag - 0.01, 0) * inv_sys_mass * 0.25
        corr_x, corr_y = multiplier * collision_norm_x, multiplier * collision_norm_y

        # Impulse Resolution

        # Relative velocity
        if rb_b_none:
            rv_x, rv_y = -rb_a.velocity.x, -rb_a.velocity.y
        elif rb_a_none:
            rv_x, rv_y = rb_b.velocity.x, rb_b.velocity.y
        else:
            rv_x, rv_y = rb_b.velocity.x - rb_a.velocity.x, rb_b.velocity.y - rb_a.velocity.y

        if (vel_along_norm := (rv_x * collision_norm_x + rv_y * collision_norm_y)) > 0:
            return

        # Calculate restitution
        e = max(0 if rb_a_none else rb_a.bounciness, 0 if rb_b_none else rb_b.bounciness)

        # Calculate impulse scalar
        j = -(1 + e) * vel_along_norm * inv_sys_mass

        # Apply the impulse
        imp_x, imp_y = j * collision_norm_x, j * collision_norm_y

        if not (rb_a_none or rb_a.static):
            rb_a.gameobj.pos.x -= inv_mass_a * corr_x
            rb_a.gameobj.pos.y -= inv_mass_a * corr_y
            rb_a.velocity.x -= inv_mass_a * imp_x
            rb_a.velocity.y -= inv_mass_a * imp_y

        if not (rb_b_none or rb_b.static):
            rb_b.gameobj.pos.x += inv_mass_b * corr_x
            rb_b.gameobj.pos.y += inv_mass_b * corr_y
            rb_b.velocity.x += inv_mass_b * imp_x
            rb_b.velocity.y += inv_mass_b * imp_y

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
        tan_x, tan_y = rv_x - vel_along_norm * collision_norm_x, rv_y - vel_along_norm * collision_norm_y

        if tan_x == tan_y == 0:
            return

        ratio = (tan_x * tan_x + tan_y * tan_y)**-.5
        tan_x, tan_y = tan_x * ratio, tan_y * ratio

        # Solve for magnitude to apply along the friction vector
        jt = -(rv_x * tan_x + rv_y * tan_y) * inv_sys_mass

        # Calculate friction impulse
        if abs(jt) < j * mu:
            fric_x, fric_y = jt * tan_x, jt * tan_y  # "Static friction"
        else:
            fric_x, fric_y = -j * tan_x * mu, -j * tan_y * mu  # "Kinetic friction"

        if not (rb_a_none or rb_a.static):
            rb_a.velocity.x -= inv_mass_a * fric_x
            rb_a.velocity.y -= inv_mass_a * fric_y

        if not (rb_b_none or rb_b.static):
            rb_b.velocity.x += inv_mass_b * fric_x
            rb_b.velocity.y += inv_mass_b * fric_y

    def fixed_update(self):
        """The update loop"""
        if not self.static:
            self.physics()
