"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from typing import TYPE_CHECKING
from rubato.classes.component import Component
from rubato.utils import Vector, Configs, Time

if TYPE_CHECKING:
    from rubato.classes.components.hitbox import CollisionInfo


class RigidBody(Component):
    """
    A RigidBody implementation with built in physics and collisions.

    Attributes:
        velocity (Vector): The velocity of the rigidbody.
        acceleration (Vector): The acceleration of the rigidbody.
        angvel (float): The angular velocity of the rigidbody.
        rotation (float): The rotation in radians.
        mass (float): The mass of the rigidbody.
        hitbox (Polygon): The hitbox of the rigidbody.
        col_type (COL_TYPE): The collision type.
        img (Image): The image to draw for the rigidbody.
        debug (bool): Whether or not debug mode is on for this rigidbody.
        grounded (bool): Whether or not the rigidbody is on the ground.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes a Rigidbody.

        Args:
            options: A rigidbody config. Defaults to the |default| for
                `RigidBody`
        """
        params = Configs.merge_params(options, Configs.rigidbody_defaults)

        super().__init__()

        self.gravity: float = params["gravity"]
        self.friction: Vector = params["friction"]
        self.max_speed: Vector = params["max_speed"]
        self.min_speed: Vector = params["min_speed"]

        self.velocity = Vector()
        self.acceleration = Vector()

        self.angvel = 0
        self.rotation = params["rotation"]

        self.mass = params["mass"]

        self.debug = params["debug"]

    def physics(self):
        self.velocity += self.acceleration * Time.delta_time("sec")

        self.sprite.pos += self.velocity * Time.delta_time("sec")

    def add_force(self, force: Vector):
        pass

    def add_impulse(self, impulse: Vector, time: int):
        pass

    def handle_collision(self, col: "CollisionInfo"):
        pass

    def update(self):
        """The update loop"""
        self.physics()
