import math, rubato as rb

rb.init(res=(150, 150), maximize=True)
scene = rb.Scene()

A, B = 0, 0


def update():
    global A, B
    z = [0] * 1760
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
                b[o] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12][N if N > 0 else 0]

    for k in range(1760):
        if b[k] != -1:  # The rubato stuff we care about, all the rest is just math
            color = rb.Color.black.lighter(int(rb.Math.lerp(0, 255, b[k] / 12)))
            pos = rb.Vector(k % 80, k // 80)
            pos -= rb.Vector(40, 12)
            pos *= 3
            rb.Draw.queue_rect(pos, 3, 3, border=color, fill=color)

        A += 0.00004
        B += 0.00002


scene.update = update

rb.begin()
