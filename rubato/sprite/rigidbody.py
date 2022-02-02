"""
The Rigidbody class contains an implementation of rigidbody physics. They
have hitboxes and can collide and interact with other rigidbodies.
"""
from typing import Callable, Union
from rubato.sprite import Sprite, Image
from rubato.utils import Vector, Time, Math, COL_TYPE, Configs, SAT, Display
from rubato.scenes import Camera
from rubato.utils.sat import CollisionInfo
from pygame import Surface
from pygame.draw import polygon


class RigidBody(Sprite):
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
            options: A rigidbody config. Defaults to the
                :ref:`default rigidbody options <defaultrigidbody>`.
        """
        self.params = Configs.merge_params(options, Configs.rigidbody_defaults)

        super().__init__({
            "pos": self.params["pos"],
            "z_index": self.params["z_index"]
        })

        self.velocity = Vector()
        self.acceleration = Vector()

        self.angvel = 0
        self.rotation = self.params["rotation"]

        self.mass = self.params["mass"]

        self.hitbox = self.params["hitbox"].clone()
        self.hitbox._pos = lambda: self.pos
        self.hitbox._rotation = lambda: self.rotation

        self.col_type = self.params["col_type"]

        self.img = self.params["img"]

        if isinstance(self.img, tuple):
            self.image = Image({
                "image_location": "empty",
                "pos": self.pos,
                "z_index": self.params["z_index"],
            })
        else:
            self.image = Image({
                "image_location": self.img,
                "pos": self.pos,
                "scale_factor": self.params["scale"],
                "z_index": self.params["z_index"],
                "rotation": self.rotation,
            })

        self.debug = self.params["debug"]

        self.grounded = False

    def physics(self):
        """A physics implementation"""
        # Update Velocity
        self.velocity.x += self.acceleration.x * Time.delta_time("sec")
        self.velocity.y += (self.acceleration.y +
                            self.params["gravity"]) * Time.delta_time("sec")

        self.velocity *= self.params["friction"]

        self.velocity.clamp(
            self.params["min_speed"],
            self.params["max_speed"],
        )
        self.velocity.absolute()

        # Update position
        self.pos.x += self.velocity.x * Time.delta_time("sec")
        self.pos.y += self.velocity.y * Time.delta_time("sec")

        # Update rotation
        self.rotation += self.angvel * Time.delta_time("sec")

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
        if col_info := SAT.overlap(self.hitbox, other.hitbox):
            # col_info is all in reference to self
            col_info.separation.round(4)

            if other.col_type == COL_TYPE.STATIC:
                self.pos -= col_info.separation
                self.grounded = Math.sign(col_info.separation.y) == 1

                if self.grounded: self.velocity.y = 0
                # FIXME: do we want this sticky behavior
                if abs(col_info.separation.x) > 0: self.velocity.x = 0
            elif self.col_type == COL_TYPE.STATIC:
                other.pos += col_info.separation
                other.grounded = Math.sign(col_info.separation.y) == -1

                if other.grounded: other.velocity.y = 0
                if abs(col_info.separation.x) > 0: other.velocity.x = 0
            else:
                self.pos -= col_info.separation / 2
                other.pos += col_info.separation / 2

        if col_info is not None:
            callback(col_info)
        return col_info

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
        if col_info := SAT.overlap(self.hitbox, other.hitbox):
            # col_info is all in reference to self
            col_info.separation.round(4)
            self.grounded = Math.sign(col_info.separation.y) == 1

            if other.col_type == COL_TYPE.STATIC:
                self.pos -= col_info.separation
            elif self.col_type == COL_TYPE.STATIC:
                other.pos += col_info.separation
            else:
                self.pos -= col_info.separation / 2
                other.pos += col_info.separation / 2

            if col_info.vertex_a is not None:
                perpendicular = (self.velocity.unit() *
                                 col_info.vertex_a.crossp().unit())
                self.angvel = -perpendicular.magnitude * self.velocity.magnitude
                self.velocity -= (col_info.separation.unit() *
                                  self.velocity.magnitude * 2)

                # self.angvel = round(
                #     Vector.cross(self.velocity.unit(),
                #                  col_info.vertex_a.unit()) *
                #     self.velocity.magnitude, 3)
                # self.velocity.y -= (col_info.vertex_a.y *
                #                     col_info.separation.unit().y * 5)
                # self.velocity.x -= (col_info.vertex_a.x *
                #                     col_info.separation.unit().x * 5)
                # vertex_a in direction of separation => velocity
                # perpendicular component => angular

            # if (self.col_type == COL_TYPE.STATIC
            #         or other.col_type == COL_TYPE.STATIC):
            #     # Static
            #     if col_info.separation.y != 0:
            #         self.velocity.y = 0
            #         other.velocity.y = 0
            #     if col_info.separation.x != 0:
            #         self.velocity.x = 0
            #         other.velocity.x = 0
            # else:
            #     # Elastic
            #     if col_info.separation.y != 0:
            #         self.velocity.invert("y")
            #         other.velocity.invert("y")
            #     if col_info.separation.x != 0:
            #         self.velocity.invert("x")
            #         other.velocity.invert("x")

        if col_info is not None:
            callback(col_info)
        return col_info

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
        col_info = SAT.overlap(self.hitbox, other.hitbox)
        if col_info is not None:
            callback(col_info)
        return col_info

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
        if (self.params["do_physics"] and self.in_frame):
            self.physics()

        self.custom_update()

    def custom_update(self):
        pass

    def draw(self, camera: Camera):
        """
        The draw loop

        Args:
            camera: The current camera
        """
        self.image.pos = self.pos
        self.image.draw(camera)

        if isinstance(self.img, tuple):
            temp = Surface(self.hitbox.bounding_box_dimensions().to_tuple())
            temp.set_alpha(self.img[3])
            temp.fill(self.img[:3])
            polygon(
                temp,
                self.img[:3],
                list(
                    map(lambda v: v.to_tuple(),
                        self.hitbox.transformed_verts())),
            )
            Display.update(
                temp,
                camera.transform(super().center_to_tl(
                    self.pos, self.hitbox.bounding_box_dimensions()) *
                                 camera.zoom),
            )

        if self.debug:
            polygon(
                Display.global_display,
                (0, 255, 0),
                list(
                    map(
                        lambda v: camera.transform(v * camera.zoom),
                        self.hitbox.real_verts(),
                    )),
                3,
            )
