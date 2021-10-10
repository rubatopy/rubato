from pgp.sprite import Sprite
from pgp.sprite import Image
from pgp.sprite import Collider
from pgp.utils import Vector, Time


class RigidBody(Sprite):
    """
    A RigidBody implementation with built in physics and collisions.

    :param options: A dictionary of options
    """
    def __init__(self, options: dict = {}):
        super().__init__(options.get("pos", Vector()))

        self.velocity = Vector()
        self.acceleration = Vector()
        self.mass = options.get("mass", 1)
        self.collider = Collider(*options.get("box", [0, 0, 0, 0]))

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

    def set_force(self, force: Vector):
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

    def collide_rb(self, other: []):
        if not isinstance(other[0], RigidBody):
            raise Exception("other must be a rigidbody list")
        hitted = self.hit(other)
        for hit in hitted:
            # if moving right
            if self.velocity[0] > 0:
                self.rectangle.right = hit.left
            if self.velocity[0] < 0:
                self.rectangle.left = hit.right
        self.rectangle.y += self.velocity[1]
        hitted = self.hit(other)
        for hit in hitted:
            # if we are going up and hit our head
            if self.velocity[1] < 0:
                self.rectangle.top = hit.bottom
            # if we are going down and hit our feet
            if self.velocity[1] > 0:
                self.velocity[1] = 0
                self.rectangle.bottom = hit.top

    def hit(self, others):
        hitted = []
        for other in others:
            if self.collider.collide(other.collider):
                hitted.append(other)
        return hitted