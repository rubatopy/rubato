import rubato as rb

# rotation
from math import cos, sin, pi


def get_xyz(x, y, z, roll, pitch, yaw):
    cospitch = cos(pitch)
    sinpitch = sin(pitch)
    cosyaw = cos(yaw)
    sinyaw = sin(yaw)
    cosroll = cos(roll)
    sinroll = sin(roll)

    _x = cospitch * cosyaw * x + (-sinpitch * cosroll + cospitch * sinyaw *
                                  sinroll) * y + (-sinpitch * -sinroll + cospitch * sinyaw * cosroll) * z

    _y = sinpitch * cosyaw * x + (cospitch * cosroll + sinpitch * sinyaw *
                                  sinroll) * y + (cospitch * -sinroll + sinpitch * sinyaw * cosroll) * z

    _z = -sinyaw * x + (cosyaw * sinroll) * y + (cosyaw * cosroll) * z

    return _x, _y, _z


# rotation

# target 54 * 54
a = 10  # a is the radius of the tube
c = 15  # c is the radius of the torus

rb.init(res=((a + c) * 2 * 10,) * 2, maximize=True)

roll = pi / 5  # spin around x-axis counter-clockwise (on screen its another up-down motion)
pitch = 0  # spin around z-axis
yaw = 0  # spin around y-axis counter-clockwise rotation (on screen it looks like ur just moving up)

# define rotation functions

half_torus: list[tuple[float, float, float]] = []


def gen_torus():
    for v in range(0, 360, 4):  # goes around the tube interval of 3 if you want it to be w/out holes
        for u in range(0, 180, 2):  # goes around the torus
            v_ = v * pi / 180
            u_ = u * pi / 180
            x = (c + a * cos(v_)) * cos(u_)
            y = (c + a * cos(v_)) * sin(u_)
            z = a * sin(v_)
            half_torus.append((x, y, z))


gen_torus()

surf = rb.Surface((a + c) * 2, (a + c) * 2, (10, 10))


def custom_draw():
    global roll, pitch, yaw
    roll += 0.0704
    pitch += 0.0352
    z_buffer = [-float("inf")] * (a + c) * 2 * (a + c) * 2
    surf.fill(rb.Color.night)

    for point in half_torus:
        x, y, z = get_xyz(*point, roll, pitch, yaw)
        for orient in (1, -1):
            _x, _y, _z = int(x) * orient, int(y) * orient, int(z) * orient
            if z_buffer[_x + (a + c) * 2 * _y] < _z:
                z_buffer[_x + (a + c) * 2 * _y] = _z
                color = rb.Color.mix(rb.Color.yellow, rb.Color.red, rb.Math.map(_z, -a - c, a + c, 0, 1), "linear")
                surf.set_pixel((_x, _y), color, blending=False)

    rb.Draw.surface(surf)


rb.Game.show_fps = True

# def custom_update():
#     global roll, pitch, yaw
#     if rb.Input.key_pressed("a"):
#         pitch += 0.01
#     if rb.Input.key_pressed("d"):
#         pitch -= 0.01

#     if rb.Input.key_pressed("w"):
#         roll -= 0.01
#     if rb.Input.key_pressed("s"):
#         roll += 0.01
#     if rb.Input.key_pressed("q"):
#         yaw += 0.01
#     if rb.Input.key_pressed("e"):
#         yaw -= 0.01

rb.Game.draw = custom_draw

rb.begin()
