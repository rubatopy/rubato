from rubato import Scene, Color, Text, wrap, Font, GameObject, Button, Raster, Time, RecurrentTask, Vector, Game, Component
import shared

scene = Scene("end_menu", background_color=Color.white)


def smooth_button_generator(button: Button, text: Text, go: GameObject):
    # go.add(button, text)

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

class SmoothButton(Component):
    def __init__(self, text: str):
        super().__init__()
        self.font_changing: RecurrentTask | None = None
        self.text_str = text
        self.text: Text = Text(self.text_str)

    def setup(self):
        self.gameobj.add(self.text)

    def increase_font_size(self, task: RecurrentTask):
        if self.font_changing is not None and self.font_changing != task:
            self.font_changing.stop()
        play_button.get(Text).font_size += 1
        if play_button.get(Text).font_size >= 64:
            task.stop()
            self.font_changing = None
            play_button.get(Text).font_size = 64
        else:
            self.font_changing = task

    def decrease_font_size(self, task: RecurrentTask):
        if self.font_changing is not None and self.font_changing != task:
            self.font_changing.stop()
        play_button.get(Text).font_size -= 1
        if play_button.get(Text).font_size <= 32:
            task.stop()
            self.font_changing = None
            play_button.get(Text).font_size = 32
        else:
            self.font_changing = task

play_button = GameObject(pos=(0, -75)).add(
    b:=Button(
        300,
        100,
        onclick=lambda: Game.set_scene("level1"),
    ),
    t:=Text("PLAY", shared.black_32),
    b2:=Button(
        300,
        100,
        onclick=lambda: Game.set_scene("level1"),
        offset=Vector(0, 100)
    ),
    t2:=Text("PLAY", shared.black_32, offset=Vector(0, 100)),
    Raster(300, 100, z_index=-1),
    Raster(300, 100, z_index=-1, offset=Vector(0, 100)),

)
for rast in play_button.get_all(Raster):
    rast.fill(Color.gray.lighter(100))

smooth_button_generator(b, t, play_button)
smooth_button_generator(b2, t2, play_button)


scene.add_ui(play_button)







# class enemy controller (Component)
# hp, mana, attack, defense, speed, etc

# enemy generator brings back go with image of enemy and enemy controller


# java
# list of enemies Enemy[] enemies = new Enemy[10];

# python, rubato
# list of enemy game objects
# enemies = [generate_enemy() for _ in range(10)]

















