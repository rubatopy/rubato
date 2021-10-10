from pgp.sprite import Sprite
from pgp.sprite import Image
from pgp.sprite import Collider
from pgp.utils import Vector, Time


class RigidBody(Sprite):
    """
    A RigidBody implementation with built in physics and collisions.

    :param options: A dictionary of options
    """

    default_options = {
        "mass": 1,
        "box": [0, 0, 0, 0],
        "do_physics": True,
        "gravity": 100,
        "max_speed": Vector(1000, 1000),
        "min_speed": Vector(-1000, -1000),
        "friction": Vector(1, 1),
        "img": ""
    }

    def __init__(self, options: dict = {}):
        super().__init__(options.get("pos", Vector()))

        self.velocity = Vector()
        self.acceleration = Vector()

        self.mass = options.get("mass", RigidBody.default_options["mass"])
        self.collider = Collider(*options.get("box", RigidBody.default_options["box"]))

        self.params = options

        self.render = Image(options.get("img", RigidBody.default_options["img"]), self.pos)

    # TODO Collisions
    def physics(self):
        """A physics implementation"""
        # Update Velocity
        self.velocity.x += self.acceleration.x * Time.delta_time("sec")
        self.velocity.y += (self.acceleration.y + self.params.get("gravity", RigidBody.default_options["gravity"])) * Time.delta_time("sec")

        self.velocity *= self.params.get("friction", RigidBody.default_options["friction"])

        self.velocity.clamp(self.params.get("min_speed", RigidBody.default_options["min_speed"]),
                            self.params.get("max_speed", RigidBody.default_options["max_speed"]))

        # Update position
        self.pos.x += self.velocity.x * Time.delta_time("sec")
        self.pos.y += self.velocity.y * Time.delta_time("sec")
        self.collider.set_topleft(*self.pos.to_tuple2())

    def set_force(self, force: Vector):
        """
        Sets a force on the RigidBody

        :param force: A Point object representing the added force to the object
        """
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass
        print(self.acceleration)

    def set_impulse(self, force: Vector, time: int):
        self.set_force(force)
        print(force)
        print(self.mass)
        Time.delayed_call(time, lambda: self.set_force(Vector()))

    def update(self):
        """The update loop"""
        if self.params.get("do_physics", RigidBody.default_options["do_physics"]):
            self.physics()

    def draw(self, camera):
        """
        The draw loop

        :param camera: The current camera
        """
        self.render.pos = self.pos
        self.render.draw(camera)

    def collide_rb(self, other: []):
        if not isinstance(other[0], RigidBody):
            raise Exception("other must be a rigidbody list")
        hitted = self.hit(other)
        for hit in hitted:
            if self.velocity[0] > 0:
                # your right becomes hits left
                pass
            if self.velocity[0] < 0:
                pass
        # self.rectangle.y += self.velocity[1]
        # hitted = self.hit(other)
        # for hit in hitted:
        #     if self.velocity[1] < 0:
        #         self.rectangle.top = hit.bottom
        #     if self.velocity[1] > 0:
        #         self.velocity[1] = 0
        #         self.rectangle.bottom = hit.top

    def hit(self, others):
        hitted = []
        for other in others:
            if self.collider.collide(other.collider):
                hitted.append(other)
        return hitted