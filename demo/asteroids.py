"""
A classic
"""
import random
from rubato import *

size = 1080
half_size = size // 2
radius = size // 40
level = 0

init(name="asteroids", res=(size, size), window_size=(size // 2, size // 2))

main = Scene()

# background
stars = Surface(size, size)
stars.fill(Color.black)
for _ in range(200):
    pos = (
        random.randint(-half_size, half_size),
        random.randint(-half_size, half_size),
    )
    stars.set_pixel(pos, Color.white)


class Timer(Component):

    def __init__(self, secs: float):
        super().__init__()
        self.secs = secs

    def remove(self):
        main.remove(self.gameobj)

    def setup(self):
        Time.delayed_call(self.remove, self.secs)


# explosion particle
expl = Surface(radius // 2, radius // 2)
expl.draw_rect((0, 0), expl.size(), Color.debug, 3)


def make_part(angle: float):
    return Particle(
        expl.clone(),
        pos=Particle.circle_shape(radius * 0.75)(angle),
        velocity=Particle.circle_direction()(angle) * random.randint(50, 100),
        rotation=random.randint(0, 360),
    )


# explosion system
expl_sys = wrap([
    ParticleSystem(new_particle=make_part, mode=ParticleSystemMode.BURST),
    Timer(5),
])


# component to move things that are out of bounds
class BoundsChecker(Component):

    def update(self):
        if self.gameobj.pos.x < Display.left - radius:
            self.gameobj.pos.x = Display.right + radius
        elif self.gameobj.pos.x > Display.right + radius:
            self.gameobj.pos.x = Display.left - radius
        if self.gameobj.pos.y > Display.top + radius:
            self.gameobj.pos.y = Display.bottom - radius
        elif self.gameobj.pos.y < Display.bottom - radius:
            self.gameobj.pos.y = Display.top + radius


# asteroid generator
def make_asteroid():
    sides = random.randint(5, 8)

    t = random.randint(-half_size, half_size)
    topbottom = random.randint(0, 1)
    side = random.randint(0, 1)
    if topbottom:
        pos = t, Display.top + (side * size + (radius if side else -radius))
    else:
        pos = Display.left + (side * size + (radius if side else -radius)), t

    direction = (-Display.center.dir_to(pos)).rotate(random.randint(-45, 45))

    main.add(
        wrap(
            [
                Polygon(
                    [
                        Vector.from_radial(
                            random.randint(
                                int(radius * .7),
                                int(radius * 0.95),
                            ),
                            -i * 360 / sides,
                        ) for i in range(sides)
                    ],
                    debug=True,
                ),
                RigidBody(
                    velocity=direction * 100,
                    ang_vel=random.randint(-30, 30),
                ),
                BoundsChecker(),
            ],
            pos,
            random.randint(0, 360),
            name="asteroid",
        )
    )


Time.schedule(RecurrentTask(make_asteroid, 1, 1))


class PlayerController(Component):

    def setup(self):
        self.speed = 250
        self.steer = 25

        self.velocity = Vector()
        self.interval = .2
        self.allowed_to_shoot = True
        self.gameobj.add(BoundsChecker())

    def update(self):
        controller_pressed = Input.controllers() and Input.controller_button(0, 0)
        if controller_pressed or Input.key_pressed("j") or Input.key_pressed("space"):
            self.shoot()

    def shoot(self):
        if self.allowed_to_shoot:
            main.add(
                wrap(
                    [
                        Circle(
                            radius // 5,
                            Color.debug,
                            trigger=True,
                            on_collide=bullet_collide,
                        ),
                        RigidBody(
                            velocity=self.gameobj.get(PlayerController).velocity \
                                + Vector.from_radial(
                                    500,
                                    self.gameobj.rotation,
                                )
                        ),
                        BoundsChecker(),
                        Timer(0.75),
                    ],
                    self.gameobj.pos,
                    self.gameobj.rotation,
                    name="bullet",
                )
            )
            self.allowed_to_shoot = False
            Time.delayed_call(
                lambda: setattr(self, "allowed_to_shoot", True),
                self.interval,
            )

    def fixed_update(self):
        c_axis_0 = Input.controller_axis(0, 0) if Input.controllers() else 0
        c_axis_1 = -Input.controller_axis(0, 1) if Input.controllers() else 0
        c_axis_0 = 0 if Input.axis_centered(c_axis_0) else c_axis_0
        c_axis_1 = 0 if Input.axis_centered(c_axis_1) else c_axis_1
        dx = c_axis_0 or \
            (-1 if Input.key_pressed("a") or Input.key_pressed("left") else (1 if Input.key_pressed("d") or Input.key_pressed("right") else 0))
        dy = c_axis_1 or \
            (1 if Input.key_pressed("w") or Input.key_pressed("up") else (-1 if Input.key_pressed("s") or Input.key_pressed("down") else 0))
        target = Vector(dx, dy)

        d_vel = target * self.speed
        steering = Vector.clamp_magnitude(d_vel - self.velocity, self.steer)

        self.velocity = Vector.clamp_magnitude(self.velocity + steering, self.speed)

        self.gameobj.pos += self.velocity * Time.fixed_delta

        if target != (0, 0):
            self.gameobj.rotation = self.velocity.angle


# player geometry, we cannot have concave polygons (yet), this gets the absolute hitbox.
full = [
    Vector.from_radial(radius, 0),
    Vector.from_radial(radius, 125),
    Vector.from_radial(radius // 4, 180),
    Vector.from_radial(radius, -125),
]
right = [full[0], full[1], full[2]]
left = [full[0], full[2], full[3]]
player_spr = Raster(radius * 2, radius * 2)
player_spr.draw_poly(full, (0, 0), Color.debug, 2, aa=True)

main.add(
    wrap(
        [
            PlayerController(),
            Polygon(right, trigger=True),
            Polygon(left, trigger=True),
            player_spr,
        ],
        Display.center,
        name="player",
    )
)


def bullet_collide(man: Manifold):
    if man.shape_b.gameobj.name == "asteroid":
        local_expl = expl_sys.clone()
        local_expl.pos = man.shape_b.gameobj.pos.clone()
        local_expl.rotation = random.randint(0, 360)
        local_expl_sys = local_expl.get(ParticleSystem)
        if isinstance(man.shape_b, Polygon):
            local_expl_sys.spread = 360 / len(man.shape_b.verts)
        local_expl_sys.start()
        main.remove(man.shape_b.gameobj)
        main.remove(man.shape_a.gameobj)
        main.add(local_expl)


def new_draw():
    Draw.surface(stars, Display.center)


Game.draw = new_draw

begin()
