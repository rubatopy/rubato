import math, rubato as rb

di, sc = 54, 3
hdi, di_sq = di // 2, di * di

rb.init("donut demo", (di * sc, di * sc))
main = rb.Scene("main", rb.Color.night)

A, B = 0, 0
s = rb.Surface(di, di, (sc, sc))


def draw():
    global A, B
    A += 0.0704
    B += 0.0352

    z = [0.0] * di_sq
    b = [-1] * di_sq
    e = math.sin(A)
    g = math.cos(A)
    n = math.sin(B)
    m = math.cos(B)
    for j in range(0, 628, 7):
        f = math.sin(j)
        d = math.cos(j)
        h = d + 2
        for i in range(0, 628, 2):
            c = math.sin(i)
            l = math.cos(i)
            D = 1 / (c * h * e + f * g + 5)
            t = c * h * g - f * e
            x = int(hdi + 30 * D * (l * h * m - t * n))
            y = int(hdi + 15 * D * (l * h * n + t * m))
            o = int(x + di * y)
            N = int(8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n))
            if di > y and y > 0 and x > 0 and di > x and D > z[o]:
                z[o] = D
                b[o] = (N + 1) if N > 0 else 0

    s.clear()
    for k in range(di_sq):
        if b[k] != -1:
            color = rb.Color.mix(rb.Color.yellow, rb.Color.red, b[k] / 12, "linear")
            pos = rb.Vector(k % di - hdi, k // di - hdi)
            s.set_pixel(pos, color, False)
    rb.Draw.surface(s)


main.draw = draw

rb.begin()
