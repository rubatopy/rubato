from rubato.sprite import Sprite, Image, Collider
from rubato.utils import Vector, Time, PMath, check_types, COL_TYPE, Polygon, SAT, Display
from rubato.scenes import Camera
from pygame import Surface
from pygame.draw import polygon


class RigidBody(Sprite):
    """
    A RigidBody implementation with built in physics and collisions.

    :param options: A dictionary of options
    """

    default_options = {
        "mass": 1,
        "hitbox": Polygon.generate_polygon(4),
        "do_physics": True,
        "gravity": 100,
        "max_speed": Vector(PMath.INFINITY, PMath.INFINITY),
        "min_speed": Vector(-PMath.INFINITY, -PMath.INFINITY),
        "friction": Vector(1, 1),
        "img": "",
        "col_type": COL_TYPE.STATIC,
        "scale": Vector(1, 1),
        "debug": False,
    }

    def __init__(self, options: dict = {}):
        check_types(RigidBody.__init__, locals())
        super().__init__(options.get("pos", Vector()))

        self.velocity = Vector()
        self.acceleration = Vector()

        self.mass = options.get("mass", RigidBody.default_options["mass"])
        # self.collider = Collider(
        #     options.get("box", RigidBody.default_options["box"]),
        #     lambda: self.pos,
        #     options.get("col_type", RigidBody.default_options["col_type"])
        # )

        self.hitbox = options.get("hitbox", RigidBody.default_options["hitbox"]).clone()
        self.hitbox._pos = lambda: self.pos

        self.col_type = options.get("col_type", RigidBody.default_options["col_type"])

        self.collides_with = []

        self.grounded = False

        self.params = options

        self.render = Image(options.get("img", RigidBody.default_options["img"]), self.pos, options.get("scale", RigidBody.default_options["scale"]))

        self.debug = options.get("debug", RigidBody.default_options["debug"])

    def physics(self):
        """A physics implementation"""
        check_types(RigidBody.physics, locals())
        # Update Velocity
        self.velocity.x += self.acceleration.x * Time.delta_time("sec")
        self.velocity.y += (self.acceleration.y +
                            self.params.get("gravity", RigidBody.default_options["gravity"])) * Time.delta_time("sec")

        self.velocity *= self.params.get("friction", RigidBody.default_options["friction"])

        self.velocity.clamp(self.params.get("min_speed", RigidBody.default_options["min_speed"]),
                            self.params.get("max_speed", RigidBody.default_options["max_speed"]), True)

        # Update position
        self.pos.x += self.velocity.x * Time.delta_time("sec")
        self.pos.y += self.velocity.y * Time.delta_time("sec")

        self.collide()

    def set_force(self, force: Vector):
        """
        Sets a force on the RigidBody.

        :param force: A Point object representing force set to the object.
        """
        check_types(RigidBody.set_force, locals())
        self.acceleration.x = force.x / self.mass
        self.acceleration.y = force.y / self.mass

    def add_force(self, force: Vector):
        """
        Adds a force to the RigidBody.

        :param force: A Point object representing the added force to the object.
        """
        check_types(RigidBody.add_force, locals())
        self.acceleration.x = self.acceleration.x + force.x / self.mass
        self.acceleration.y = self.acceleration.y + force.y / self.mass

    def collide(self):
        """A simple collision engine for most use cases."""
        self.grounded = False
        for rigid in self.collides_with:
            if col_info := SAT.overlap(self.hitbox, rigid.hitbox):
                # col_info is all in reference to self
                col_info.separation.round(4)
                # TODO make grounded check
                # Static
                if self.col_type == COL_TYPE.STATIC or rigid.col_type == COL_TYPE.STATIC:
                    self.pos -= col_info.separation
                    if col_info.separation.y != 0:
                        self.velocity.y = 0
                    if col_info.separation.x != 0:
                        self.velocity.x = 0
                # Elastic
                elif self.col_type == COL_TYPE.ELASTIC and rigid.col_type == COL_TYPE.ELASTIC:
                    self.pos -= col_info.separation
                    if col_info.separation.y != 0:
                        self.velocity.invert("y")
                    if col_info.separation.x != 0:
                        self.velocity.invert("x")

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

        if self.debug:
            polygon(Display.global_display, (0, 255, 0), list(map(lambda v: (v.x, v.y), self.hitbox.real_verts())), 3)
