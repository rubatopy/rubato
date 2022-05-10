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
        self.steer = .02 * const
        self.wander = 0.001 * const

        self.position = self.gameobj.pos
        self.velocity = Vector(1, 1)
        self.desired_direction = Vector(1, 0)
        self.target = Display.bottom_right

    def update(self):
        self.desired_direction = (self.target - self.position).unit()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(self.velocity + acceleration * Time.delta_time, self.speed)
        self.position += self.velocity * Time.delta_time

        self.gameobj.pos = self.position
        self.gameobj.rotation = -math.math.degrees(self.velocity.angle + math.math.pi / 2)

    def update2(self):
        self.desired_direction = (self.desired_direction + Vector.random_inside_unit_circle * self.wander).unit()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(self.velocity + acceleration * Time.delta_time, self.speed)
        self.position += self.velocity * Time.delta_time / 100

        self.gameobj.pos = self.position
        self.gameobj.rotation = -math.math.degrees(self.velocity.angle + math.math.pi / 2)

        print(self.velocity.angle, acceleration, self.desired_direction)


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
