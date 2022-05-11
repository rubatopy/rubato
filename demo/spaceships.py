"""
A demo that shows how to extend the GameObject and Component classes.
"""
import math

from rubato import *
# pylint: disable=all
init({
    "name": "Point drawing",
    "target_fps": 24,
    "res": Vector(800, 600),
    "window_size": Vector(800, 600),
})
main_scene = Scene()


class SpaceshipComp(Component):
    """
    A spaceship component.
    """

    def setup(self):
        const = .1
        self.speed = 2 * const
        self.steer = .2 * const
        self.wander = 2 * const

        self.position = self.gameobj.pos
        self.velocity = Vector(1, 1)
        self.desired_direction = Vector(0, 0)
        self.target = Display.bottom_right

    def update(self):
        self.update_wander()

    def update_target(self):
        self.desired_direction = (self.target - self.position).unit()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(self.velocity + acceleration * Time.delta_time, self.speed)
        self.position += self.velocity * Time.delta_time

        if (new := self.position.clamp(Display.bottom_left + 10, Display.top_right - 10)) != self.position:
            print("ahhh")
            self.position = new
            self.velocity = -self.velocity

        self.gameobj.pos = self.position
        self.gameobj.rotation = -math.degrees(self.velocity.angle + math.math.pi / 2)

    def update_wander(self):
        self.desired_direction = (self.desired_direction + Vector.random_inside_unit_circle * self.wander).unit()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(self.velocity + acceleration * Time.delta_time, self.speed)
        self.position += self.velocity * Time.delta_time
        if (new := self.position.clamp(Display.top_left, Display.bottom_right)) != self.position:
            self.position = new
            print(self.velocity.dir_to(Display.center))
            self.velocity = Vector.from_radial(self.speed, Vector.angle_between(self.velocity, Display.center))
            print(self.velocity.dir_to(Display.center))
            # input("")
            self.position += self.velocity * Time.delta_time * 4

        self.gameobj.pos = self.position
        self.gameobj.rotation = -math.degrees(self.velocity.angle + math.math.pi / 2)


class Spaceship(GameObject):
    """
    A spaceship.
    """

    def __init__(self):
        super().__init__({
            "pos": Display.center,
        })
        self.image = Image({"rel_path": "sprites/spaceship/spaceship.png"})
        self.add(self.image)
        self.sc = SpaceshipComp()
        self.add(self.sc)


space_ship = Spaceship()

main_scene.add(space_ship)


def update():
    # if Input.any_mouse_button_pressed():
    space_ship.sc.target = Input.get_mouse_pos()


main_scene.update = update

begin()
