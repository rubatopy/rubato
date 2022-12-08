"""
Prototype mathematics in rubato
"""
import rubato as rb
import math

shape: list[tuple[float, float, float]] = []  # list of the points on the shape
roll, pitch, yaw = 0, 0, 0  # x, z, and y counter-clockwise rotation, respectively
surf_dim = 50  # diameter of the surface holding the shape

rb.init(
    "Donut Demo",
    res=(surf_dim, surf_dim),
    window_size=(500, 500),
    target_fps=60,
)
surf = rb.Surface(surf_dim, surf_dim)

# creates a donut and populates the shape list
rad, thick = 12, 7  # radius and thickness of the donut
mag = rad + thick  # maximum distance of any pt to the origin
for i in range(0, 360, 4):  # revolve around a circle
    for j in range(0, 360, 2):  # revolve the circle around the tube
        v, u = math.radians(i), math.radians(j)
        x = (rad + thick * math.cos(v)) * math.cos(u)
        y = (rad + thick * math.cos(v)) * math.sin(u)
        z = thick * math.sin(v)
        shape.append((x, y, z))


def rotate_pt(x, y, z, roll, pitch, yaw):
    cosp, sinp = math.cos(pitch), math.sin(pitch)
    cosy, siny = math.cos(yaw), math.sin(yaw)
    cosr, sinr = math.cos(roll), math.sin(roll)

    rx = (cosp * siny * sinr - sinp * cosr) * y + (sinp * sinr + cosp * siny * cosr) * z + cosp * cosy * x
    ry = (cosp * cosr + sinp * siny * sinr) * y + (sinp * siny * cosr - cosp * sinr) * z + sinp * cosy * x
    rz = (cosy * sinr) * y + (cosy * cosr) * z - siny * x

    return int(rx), int(ry), int(rz)


def update():
    global roll, pitch, yaw
    roll += 0.0704
    pitch += 0.0352


def draw():
    z_buffer = [-float("inf")] * (surf_dim**2)
    surf.fill(rb.Color.night)
    for point in shape:
        x, y, z = rotate_pt(*point, roll, pitch, yaw)
        if z_buffer[x + surf_dim * y] < z:
            z_buffer[x + surf_dim * y] = z
            color = rb.Color.mix(
                rb.Color.yellow,
                rb.Color.red,
                rb.Math.map(z, -mag, mag, 0, 1),
                "linear",
            )
            surf.set_pixel((x, y), color, False)
    rb.Draw.surface(surf)


rb.Game.update = update
rb.Game.draw = draw
rb.begin()
