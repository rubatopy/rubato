from rubato import Display, Vector, Scene, Color

level_size = int(Display.res.x * 2)
portal_location = Vector(Display.left + level_size - 128, 0)

scene = Scene("level2", background_color=Color.cyan.lighter())


def won():
    pass
