"""
A demo that shows how to extend the GameObject and Component classes.
"""
import math

from rubato import *

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
        self.desired_direction = Vector(-1, 0)
        self.target = Display.bottom_right

    def update(self):
        self.update_target()

    def update_target(self):
        self.desired_direction = (self.target - self.position).unit()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(self.velocity + acceleration * Time.delta_time, self.speed)
        self.position += self.velocity * Time.delta_time

        self.gameobj.pos = self.position
        self.gameobj.rotation = -math.degrees(self.velocity.angle + math.pi / 2)

    def update_wander(self):
        self.desired_direction = (self.desired_direction + Vector.random_inside_unit_circle * self.wander).unit()

        desired_velocity = self.desired_direction * self.speed
        steering_force = (desired_velocity - self.velocity) * self.steer
        acceleration = Vector.clamp_magnitude(steering_force, self.steer)  # / self.mass

        self.velocity = Vector.clamp_magnitude(self.velocity + acceleration * Time.delta_time, self.speed)
        self.position += self.velocity * Time.delta_time
        if (new := self.position.clamp(Display.top_left, Display.bottom_right)) != self.position:
            self.position = new
            self.velocity = Vector.from_radial(self.speed, self.position.dir_to(Display.center).angle)
            self.desired_direction = self.velocity.unit()
            self.position += self.velocity * Time.delta_time

        self.gameobj.pos = self.position
        self.gameobj.rotation = -math.degrees(self.velocity.angle + math.pi / 2)


space_ship = GameObject({
    "pos": Display.center
}).add(Image({"rel_path": "sprites/spaceship/spaceship.png"})).add(SpaceshipComp())

sc_comp = space_ship.get(SpaceshipComp)
main_scene.add(space_ship)


def update():
    # if Input.any_mouse_button_pressed():
    sc_comp.target = Input.get_mouse_pos()


main_scene.update = update

begin()
