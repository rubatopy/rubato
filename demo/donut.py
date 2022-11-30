import math, rubato as rb

rb.init(res=(150, 150), window_size=(450, 450))
main = rb.Scene("main", rb.Color.night)

A, B = 0, 0
z, b = [], []
s = rb.Surface(80, 80, (3, 3))


def draw():
    global A, B, z, b

    z = [0.0] * 1760
    b = [-1] * 1760
    for j in range(0, 628, 7):
        for i in range(0, 628, 2):
            c = math.sin(i)
            d = math.cos(j)
            e = math.sin(A)
            f = math.sin(j)
            g = math.cos(A)
            h = d + 2
            D = 1 / (c * h * e + f * g + 5)
            l = math.cos(i)
            m = math.cos(B)
            n = math.sin(B)
            t = c * h * g - f * e
            x = int(40 + 30 * D * (l * h * m - t * n))
            y = int(12 + 15 * D * (l * h * n + t * m))
            o = int(x + 80 * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
            if 22 > y and y > 0 and x > 0 and 80 > x and D > z[o]:
                z[o] = D
                b[o] = (N + 1) if N > 0 else 0

    s.clear()
    for k in range(1760):
        if b[k] != -1:
            color = rb.Color.mix(rb.Color.yellow, rb.Color.red, b[k] / 12, "linear")
            pos = rb.Vector(k % 80 - 40, k // 80 - 12)
            s.set_pixel(pos, color, False)

    A += 0.0704
    B += 0.0352

    rb.Draw.surface(s)


main.draw = draw

rb.begin()
