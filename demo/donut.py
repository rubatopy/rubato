"""
Prototype mathematics in rubato
"""

import rubato as rb
import math

thickness = 10  # a is the thickness of the donut
radius = 15  # c is the radius of the donut
angle_of_tube = 360  # How much of the tube is visible (in degrees)
angle_of_donut = 360  # How much of the donut is visible (in degrees)

rb.init(res=(500, 500), maximize=True, target_fps=60)
rb.Game.show_fps = True


def rotate_pt(x, y, z, roll, pitch, yaw):
    cosp, sinp = math.cos(pitch), math.sin(pitch)
    cosy, siny = math.cos(yaw), math.sin(yaw)
    cosr, sinr = math.cos(roll), math.sin(roll)

    rx = cosp * cosy * x + (cosp * siny * sinr - sinp * cosr) * y + (sinp * sinr + cosp * siny * cosr) * z
    ry = sinp * cosy * x + (cosp * cosr + sinp * siny * sinr) * y + (sinp * siny * cosr - cosp * sinr) * z
    rz = (cosy * sinr) * y + (cosy * cosr) * z - siny * x

    return int(rx), int(ry), int(rz)


roll = 0  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0  # spin around z-axis
yaw = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)

deg_to_rad = math.pi / 180

shape: list[tuple[float, float, float]] = []

# calculates the points on a donut with no rotation centered on the origin
for v in range(0, angle_of_tube, 4):  # goes around the tube interval of 3 if you want it to be w/out holes
    for u in range(0, angle_of_donut, 2):  # goes around the torus
        v_ = v * deg_to_rad
        u_ = u * deg_to_rad
        x = (radius + thickness * math.cos(v_)) * math.cos(u_)
        y = (radius + thickness * math.cos(v_)) * math.sin(u_)
        z = thickness * math.sin(v_)
        shape.append((x, y, z))

surf = rb.Surface((thickness + radius) * 2, (thickness + radius) * 2, (10, 10))


def custom_update():
    global roll, pitch, yaw
    roll += 0.0704
    pitch += 0.0352
    # Updates the roll and yaw in radians


def custom_draw():
    z_buffer = [-float("inf")] * ((thickness + radius) * 2)**2
    surf.fill(rb.Color.night)

    # rotates the points centered on the origin, then draws them
    for point in shape:
        x, y, z = rotate_pt(*point, roll, pitch, yaw)
        if z_buffer[x + (thickness + radius) * 2 * y] < z:
            z_buffer[x + (thickness + radius) * 2 * y] = z
            color = rb.Color.mix(
                rb.Color.yellow, rb.Color.red, rb.Math.map(z, -thickness - radius, thickness + radius, 0, 1), "linear"
            )
            surf.set_pixel((x, y), color, False)

    rb.Draw.queue_surface(surf)


rb.Game.update = custom_update
rb.Game.draw = custom_draw
rb.begin()
