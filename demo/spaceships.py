"""
A demo that shows how to extend the GameObject and Component classes.
"""
from rubato import *

init(
    name="Point drawing",
    target_fps=24,
    res=Vector(800, 600),
    size=Vector(800, 600),
)

main_scene = Scene()


class SpaceshipComp(Component):
    """
    A spaceship component.
    """

    def setup(self):
        const = .1
        self.speed = 2 * const
        self.steer = .2 * const
        self.wander = 1 * const

        self.velocity = Vector(1, 1)
        self.desired_direction = Vector(-1, 0)
        self.target = Display.bottom_right

    def update_target(self):
        self.desired_direction = (self.target - self.gameobj.pos).normalized()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(
            self.velocity + acceleration * Time.sec_to_milli(Time.delta_time), self.speed
        )
        self.gameobj.pos += self.velocity * Time.sec_to_milli(Time.delta_time)

        # self.gameobj.rotation = self.velocity.angle
        self.gameobj.rotation = 90

    def update_wander(self):
        self.desired_direction = (self.desired_direction +
                                  Vector.random_inside_unit_circle() * self.wander).normalized()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(
            self.velocity + acceleration * Time.sec_to_milli(Time.delta_time), self.speed
        )
        self.gameobj.pos += self.velocity * Time.sec_to_milli(Time.delta_time)
        if (new := self.gameobj.pos.clamp(Display.top_left, Display.bottom_right)) != self.gameobj.pos:
            self.gameobj.pos = new
            self.velocity = Vector.from_radial(self.speed, self.gameobj.pos.dir_to(Display.center).angle)
            self.desired_direction = self.velocity.normalized()
            self.gameobj.pos += self.velocity * Time.sec_to_milli(Time.delta_time)

        self.gameobj.rotation = self.velocity.angle


space_ship = GameObject(pos=Display.center).add(Image(rel_path="sprites/spaceship/spaceship.png")).add(SpaceshipComp())

sc_comp = space_ship.get(SpaceshipComp)
main_scene.add(space_ship)


def update():
    if Input.key_pressed("w"):
        sc_comp.update = sc_comp.update_wander
    if Input.key_pressed("t"):
        sc_comp.update = sc_comp.update_target

    sc_comp.target = Input.get_mouse_pos()

main_scene.update = update

begin()
