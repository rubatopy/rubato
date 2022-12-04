import math, rubato as rb

A, B = 0, 0
di, sc = 54, 3
hdi, di_sq = di // 2, di * di
res = rb.Vector(di * sc, di * sc)

rb.init("donut demo", res, res * 3)
s = rb.Surface(di, di, (sc, sc))

rb.Game.show_fps = True

def draw():
    global A, B
    A += 0.0704
    B += 0.0352

    z = [0.0] * di_sq
    e, g = math.sin(A), math.cos(A)
    n, m = math.sin(B), math.cos(B)
    for j in range(0, 628, 7):
        f, d = math.sin(j / 100), math.cos(j / 100)
        h = d + 1.5
        for i in range(0, 628, 2):
            c, l = math.sin(i / 100), math.cos(i / 100)
            D = 3 / (c * h * e + f * g + 5)
            t = c * h * g - f * e
            x = int(hdi + 10 * D * (l * h * m - t * n))
            y = int(hdi + 10 * D * (l * h * n + t * m))
            o = int(x + di * y)
            if o < di_sq and D > z[o]:
                z[o] = D

    s.fill(rb.Color.night)
    for k in range(di_sq):
        if z[k] != 0:
            color = rb.Color.mix(rb.Color.yellow, rb.Color.red, z[k], "linear")
            s.set_pixel((k % di - hdi, k // di - hdi), color, False)
    rb.Draw.surface(s)


rb.Game.draw = draw
rb.begin()
