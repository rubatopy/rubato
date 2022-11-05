from rubato import init, begin, Draw, Display, Surface, Game, Vector as V, Color as C

width, height = 32, 32
gridx, gridy = 4, 4
main_c = C.red
second_c = C.green
bg_c = C.blue
init("Surface Demo", V(width * gridx, height * gridy), V(1000, 1000))

shapes = [Surface(width, height) for _ in range(gridx * gridy)]

for shape in shapes:
    shape.draw_rect(V(0, 0), V(width, height), fill=bg_c)

col = 0

line_p = (V(-12, 9), V(12, -9))

shapes[col].draw_line(*line_p, main_c)
shapes[gridx + col].draw_line(*line_p, main_c, True)
shapes[2 * gridx + col].draw_line(*line_p, main_c, thickness=3)
shapes[3 * gridx + col].draw_line(*line_p, main_c, True, 2, True)

col += 1

rect_d = (V(0, 0), V(width - 8, height - 8))

shapes[col].draw_rect(*rect_d, main_c)
shapes[gridx + col].draw_rect(*rect_d, main_c)
shapes[2 * gridx + col].draw_rect(*rect_d, main_c, 3, second_c)
shapes[3 * gridx + col].draw_rect(*rect_d, main_c, 2, second_c, True)

col += 1

circle_d = (V(0, 0), (width // 2) - 2)

shapes[col].draw_circle(*circle_d, main_c)
shapes[gridx + col].draw_circle(*circle_d, main_c, aa=True)
shapes[2 * gridx + col].draw_circle(*circle_d, main_c, 3, second_c)
shapes[3 * gridx + col].draw_circle(*circle_d, main_c, 2, second_c, True)

col += 1

points = ([v for v in V.poly(6, (width / 2) - 2)], (0, 0))

shapes[col].draw_poly(*points, main_c)
shapes[gridx + col].draw_poly(*points, main_c, aa=True)
shapes[2 * gridx + col].draw_poly(*points, main_c, 3, second_c)
shapes[3 * gridx + col].draw_poly(*points, main_c, 2, second_c, True)


def update():
    for i in range(len(shapes)):
        Draw.queue_surface(
            shapes[i], Display.top_left + ((i % gridx) * width + (width / 2), -(i // gridx) * height - (height / 2))
        )


Game.update = update

begin()
