from pgp.sprite import Sprite, Image, Collider
from pgp.utils import Vector, Time, PMath, check_types
from pgp.scenes import Camera


class RigidBody(Sprite):
    """
    A RigidBody implementation with built in physics and collisions.

    :param options: A dictionary of options
    """

    default_options = {
        "mass": 1,
        "box": [0, 0, 16, 16],
        "do_physics": True,
        "gravity": 100,
        "max_speed": Vector(PMath.INFINITY, PMath.INFINITY),
        "min_speed": Vector(-PMath.INFINITY, -PMath.INFINITY),
        "friction": Vector(1, 1),
        "img": ""
    }

    def __init__(self, options: dict = {}):
        check_types(RigidBody.__init__, locals())
        super().__init__(options.get("pos", Vector()))

        self.velocity = Vector()
        self.acceleration = Vector()

        self.mass = options.get("mass", RigidBody.default_options["mass"])
        self.collider = Collider(options.get("box", RigidBody.default_options["box"]), lambda: self.pos)

        self.collides_with = []

        self.params = options

        self.render = Image(options.get("img", RigidBody.default_options["img"]), self.pos)

    # TODO Collisions
    def physics(self):
        """A physics implementation"""
        check_types(RigidBody.physics, locals())
        # Update Velocity
        self.velocity.x += self.acceleration.x * Time.delta_time("sec")
        self.velocity.y += (self.acceleration.y + self.params.get("gravity", RigidBody.default_options[
            "gravity"])) * Time.delta_time("sec")

        self.velocity *= self.params.get("friction", RigidBody.default_options["friction"])

        self.velocity.clamp(self.params.get("min_speed", RigidBody.default_options["min_speed"]),
                            self.params.get("max_speed", RigidBody.default_options["max_speed"]), True)

        # Update position
        self.pos.x += self.velocity.x * Time.delta_time("sec")
        self.pos.y += self.velocity.y * Time.delta_time("sec")

        for rigid in self.collides_with:
            if side := self.collider.overlap(rigid.collider, False):
                if side == "top" or side == "bottom":
                    self.velocity.invert("y")
                if side == "right" or side == "left":
                    self.velocity.invert("x")

        self.velocity *= self.params.get("friction", RigidBody.default_options["friction"])

        self.velocity.clamp(self.params.get("min_speed", RigidBody.default_options["min_speed"]),
                            self.params.get("max_speed", RigidBody.default_options["max_speed"]), True)

        # Update position
        self.pos.x += self.velocity.x * Time.delta_time("sec")
        self.pos.y += self.velocity.y * Time.delta_time("sec")



    def set_force(self, force: Vector):
        """
        Sets a force on the RigidBody.

        :param force: A Point object representing the added force to the object.
        """
        check_types(RigidBody.set_force, locals())
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass

    def set_impulse(self, force: Vector, time: int):
        """
        Sets an impulse on the rigid body

        :param force: The force of the impulse
        :param time: The duration of the impulse
        """
        check_types(RigidBody.set_impulse, locals())
        self.set_force(force)
        Time.delayed_call(time, lambda: self.set_force(Vector()))

    def update(self):
        """The update loop"""
        check_types(RigidBody.update, locals())
        if self.params.get("do_physics", RigidBody.default_options["do_physics"]):
            self.physics()

    def draw(self, camera: Camera):
        """
        The draw loop

        :param camera: The current camera
        """
        check_types(RigidBody.draw, locals())
        self.render.pos = self.pos
        self.render.draw(camera)
