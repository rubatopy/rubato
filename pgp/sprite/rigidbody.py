from pgp.sprite.sprite import Sprite
from pgp.sprite.image import Image
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
        self.box = options.get("box", RigidBody.default_options["box"])

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

    def set_force(self, force: Vector):
        """
        Sets a force on the RigidBody

        :param force: A Point object representing the added force to the object
        """
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass

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
