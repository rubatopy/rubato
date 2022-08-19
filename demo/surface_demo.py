from rubato import init, begin, Vector as V, Draw, Surface, Color as C, Game

width, height = 32, 32
gridx, gridy = 4, 4
init("Surface Demo", V(width * gridx, height * gridy), V(1000, 1000))

shapes = [Surface(width, height) for _ in range(gridx * gridy)]

for shape in shapes:
    shape.draw_rect(V(0, 0), V(width, height), C.blue, fill=C.blue)

col = 0

shapes[col].draw_line(V(4, 6), V(width - 8, height - 12), C.red)
shapes[gridx + col].draw_line(V(4, 6), V(width - 8, height - 12), C.red, thickness=3)
shapes[2 * gridx + col].draw_line(V(4, 6), V(width - 8, height - 12), C.red, True)
shapes[3 * gridx + col].draw_line(V(4, 6), V(width - 8, height - 12), C.red, True, blending=True)

col += 1

shapes[col].draw_rect(V(4, 4), V(width - 8, height - 8), C.red)
shapes[gridx + col].draw_rect(V(4, 4), V(width - 8, height - 8), C.red, 3)
shapes[2 * gridx + col].draw_rect(V(4, 4), V(width - 8, height - 8), C.red, 3, C.green)
shapes[3 * gridx + col].draw_rect(V(4, 4), V(width - 8, height - 8), C.red, 2, C.green, True)

col += 1

shapes[col].draw_circle(V(width / 2, height / 2), (width // 2) - 2, C.red)
shapes[gridx + col].draw_circle(V(width / 2, height / 2), (width // 2) - 2, C.red, 3, C.green)
shapes[2 * gridx + col].draw_circle(V(width / 2, height / 2), (width // 2) - 2, C.red, aa=True)
shapes[3 * gridx +
       col].draw_circle(V(width / 2, height / 2), (width // 2) - 2, C.red, fill=C.green, aa=True, blending=True)

col += 1

points = [v + V(width / 2, height / 2) for v in V.poly(6, (width / 2) - 2)]

shapes[col].draw_poly(points, C.red)
shapes[gridx + col].draw_poly(points, C.red, 3, C.green)
shapes[2 * gridx + col].draw_poly(points, C.red, aa=True)
shapes[3 * gridx + col].draw_poly(points, C.red, fill=C.green, aa=True, blending=True)


def update():
    for i in range(len(shapes)):
        Draw.queue_surf(shapes[i], V((i % gridx) * width + (width / 2), (i // gridx) * height + (height / 2)))


Game.update = update

begin()