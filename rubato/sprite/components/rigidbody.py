"""
The Rigidbody component contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from typing import Callable, Union
from rubato.sprite import Component
from rubato.utils import Vector, Time, Math, COL_TYPE, Configs, SAT, Display
from rubato.utils.sat import CollisionInfo
from pygame.draw import polygon
import rubato as rb


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

        self.velocity = Vector()
        self.acceleration = Vector()

        self.angvel = 0
        self.rotation = params["rotation"]

        self.mass = params["mass"]

        self.hitbox = params["hitbox"].clone()
        self.hitbox._pos = lambda: self.sprite.pos
        self.hitbox._rotation = lambda: self.rotation

        self.col_type = params["col_type"]

        self.do_physics = params["do_physics"]

        self.debug = params["debug"]

        self.grounded = False

    def physics(self):
        """Runs a simulation step on the rigidbody"""
        pass

    def set_force(self, force: Vector):
        """
        Sets a force on the RigidBody.

        Args:
            force: A force to set to the object.
        """
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass

    def add_force(self, force: Vector):
        """
        Adds a force to the RigidBody.

        Args:
            force: A force to add the object.
        """
        self.acceleration.x = self.acceleration.x + force.x / self.mass
        self.acceleration.y = self.acceleration.y + force.y / self.mass

    def collide(
            self,
            other: "RigidBody",
            callback: Callable = lambda c: None) -> Union[CollisionInfo, None]:
        """
        A simple collision engine for most use cases.

        Args:
            other: The other rigidbody to collide with.
            callback: The function to run when a collision is detected.
                Defaults to None.

        Returns:
            Union[CollisionInfo, None]: Returns a collision info object if a
            collision is detected or nothing if no collision is detected.
        """
        self.grounded = False
        if collision := SAT.overlap(self.hitbox, other.hitbox):
            # collision is all in reference to self
            collision.sep.round(4)

            if other.col_type == COL_TYPE.STATIC:
                self.sprite.pos -= collision.sep
                self.grounded = Math.sign(collision.sep.y) == 1

                if self.grounded: self.velocity.y = 0
                # FIXME: do we want this sticky behavior
                if abs(collision.sep.x) > 0: self.velocity.x = 0
            elif self.col_type == COL_TYPE.STATIC:
                other.pos += collision.sep
                other.grounded = Math.sign(collision.sep.y) == -1

                if other.grounded: other.velocity.y = 0
                if abs(collision.sep.x) > 0: other.velocity.x = 0
            else:
                self.sprite.pos -= collision.sep / 2
                other.pos += collision.sep / 2

        if collision is not None:
            callback(collision)
        return collision

    def bounce(
            self,
            other: "RigidBody",
            callback: Callable = lambda c: None) -> Union[CollisionInfo, None]:
        """
        A more complex collision resolution system with angular momentums.

        Args:
            other: The other rigidbody to collide with.
            callback: The function to run when a collision is detected.
                Defaults to None.

        Returns:
            Union[CollisionInfo, None]: Returns a collision info object if a
            collision is detected or nothing if no collision is detected.
        """
        self.grounded = False
        if collision := SAT.overlap(self.hitbox, other.hitbox):
            # collision is all in reference to self
            collision.sep.round(4)
            self.grounded = Math.sign(collision.sep.y) == 1

            if other.col_type == COL_TYPE.STATIC:
                self.sprite.pos -= collision.sep
            elif self.col_type == COL_TYPE.STATIC:
                other.pos += collision.sep
            else:
                self.sprite.pos -= collision.sep / 2
                other.pos += collision.sep / 2

        if collision is not None:
            callback(collision)
        return collision

    def overlap(
            self,
            other: "RigidBody",
            callback: Callable = lambda c: None) -> Union[CollisionInfo, None]:
        """
        Checks for a collision but does not fix it.

        Args:
            other: The other rigidbody to overlap.
            callback: The function for run if an overlap is detected.
                Defaults to None.

        Returns:
            Union[CollisionInfo, None]: Returns a collision info object if a
            collision is detected or nothing if no collision is detected.
        """
        collision = SAT.overlap(self.hitbox, other.hitbox)
        if collision is not None:
            callback(collision)
        return collision

    def set_impulse(self, force: Vector, time: int):
        """
        Sets an impulse on the rigid body

        Args:
            force: The force of the impulse
            time: The duration of the impulse
        """
        self.set_force(force)
        Time.delayed_call(time, lambda: self.set_force(Vector()))

    def update(self):
        """The update loop"""
        if (self.do_physics and self.sprite.in_frame):
            self.physics()

        self.draw()

    def draw(self):
        """
        The draw loop

        Args:
            camera: The current camera
        """
        if self.debug:
            polygon(
                Display.global_display,
                (0, 255, 0),
                list(
                    map(
                        lambda v: rb.game.scenes.current_scene.camera.
                        transform(v * rb.game.scenes.current_scene.camera.zoom
                                  ),
                        self.hitbox.real_verts(),
                    )),
                3,
            )
