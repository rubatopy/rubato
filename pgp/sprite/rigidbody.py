from pgp.sprite.sprite import Sprite
from pgp.sprite.image import Image
from pgp.utils import Point, Time


class RigidBody(Sprite):
    """
    A RigidBody implementation with built in physics and collisions.

    :param options: A dictionary of options
    """
    def __init__(self, options: dict = {}):
        super().__init__(options.get("pos", Point()))

        self.velocity = Point()
        self.acceleration = Point()
        self.mass = options.get("mass", 1)
        self.box = options.get("box", [0, 0, 0, 0])

        self.render = Image(options.get("img", ""), self.pos)

    # TODO Collisions
    def physics(self):
        """A physics implementation"""
        # Update Velocity
        self.velocity.x += self.acceleration.x * Time.delta_time("sec")
        self.velocity.y += self.acceleration.y * Time.delta_time("sec")

        # Update position
        self.pos.x += self.velocity.x * Time.delta_time("sec")
        self.pos.y += self.velocity.y * Time.delta_time("sec")

        # Gravity for the next frame
        self.acceleration.y = 98

    def set_force(self, force: Point):
        """
        Sets a force on the RigidBody

        :param force: A Point object representing the added force to the object
        """
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass

    def update(self):
        """The update loop"""
        self.physics()
        self.render.pos = self.pos

    def draw(self, camera):
        """
        The draw loop

        :param camera: The current camera
        """
        self.render.draw(camera)
