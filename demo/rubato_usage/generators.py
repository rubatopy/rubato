from rubato import Scene, Color, Text, Font, GameObject, Button, Raster, Time, RecurrentTask, Vector, Game
import rubato as rb

rb.init()
scene = Scene("menu", background_color=Color.white)

black_32 = Font(size=32)


def smooth_button_generator(onclick: callable, text: str, go: GameObject, offset: Vector = Vector(0, 0)):
    # generate the components
    button = Button(
        300,
        100,
        onclick=lambda: onclick,
        offset=offset,
        z_index=-1,
    )
    text = Text(text, font=black_32, offset=offset)
    # add the components to the game object
    go.add(button, text)

    # link their behaviours
    button.onhover = lambda: Time.recurrent_call(increase_font_size, 3)
    button.onexit = lambda: Time.recurrent_call(decrease_font_size, 3)
    font_changing: RecurrentTask | None = None

    def increase_font_size(task: RecurrentTask):
        nonlocal font_changing
        if font_changing is not None and font_changing != task:
            font_changing.stop()
        text.font_size += 1
        if text.font_size >= 64:
            task.stop()
            font_changing = None
            text.font_size = 64
        else:
            font_changing = task

    def decrease_font_size(task: RecurrentTask):
        nonlocal font_changing
        if font_changing is not None and font_changing != task:
            font_changing.stop()
        text.font_size -= 1
        if text.font_size <= 32:
            task.stop()
            font_changing = None
            text.font_size = 32
        else:
            font_changing = task


offset = Vector(0, 200)

play_button = GameObject(pos=(0, -75)).add(
    Raster(300, 100, z_index=-1),
    Raster(300, 100, z_index=-1, offset=offset),
)

for rast in play_button.get_all(Raster):
    rast.fill(Color.gray.lighter(100))

smooth_button_generator(lambda: Game.set_scene("level1"), "level 1", play_button, offset=offset)
smooth_button_generator(lambda: Game.set_scene("level2"), "level 2", play_button)


scene.add_ui(play_button)


rb.begin()


# class enemy controller (Component)
# hp, mana, attack, defense, speed, etc

# enemy generator brings back go with image of enemy and enemy controller


# java
# list of enemies Enemy[] enemies = new Enemy[10];

# python, rubato
# list of enemy game objects
# enemies = [generate_enemy() for _ in range(10)]
