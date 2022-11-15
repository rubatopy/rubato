import rubato as rb
from data_scene import DataScene
from player_controller import PlayerController
from random import randint

black_32 = rb.Font(size=32)
white_32 = rb.Font(size=32, color=rb.Color.white)
start_time = 0

##### COLORS #####

dirt_color = rb.Color.from_hex("#e58e26")
platform_color = rb.Color.from_hex("#e58e26")
wood_color = rb.Color.from_hex("#e58e26")
background_color = rb.Color.from_hex("#0c2461")


##### FOG EFFECT #####
class VignetteScroll(rb.Component):

    def update(self):
        self.gameobj.pos = player.pos


vignette = rb.GameObject(z_index=1000).add(rb.Image("files/vignette/vignette.png"), VignetteScroll())

##### PLAYER #####

# Create the player
player = rb.GameObject(z_index=1)

# Create animation and initialize states
p_animation = rb.Spritesheet.from_folder(
    path="files/dino",
    sprite_size=rb.Vector(24, 24),
    default_state="idle",
)
p_animation.scale = rb.Vector(4, 4)
p_animation.fps = 10  # The frames will change 10 times a second
player.add(p_animation)  # Add the animation component to the player

player.add(
    # add a hitbox to the player with the collider
    rb.Rectangle(width=40, height=64, tag="player"),
    # add a ground detector
    rb.Rectangle(
        width=34,
        height=2,
        offset=rb.Vector(0, -32),
        trigger=True,
        tag="player_ground_detector",
    ),
    # add a rigidbody to the player
    rb.RigidBody(gravity=rb.Vector(y=rb.Display.res.y * -1.5), pos_correction=1, friction=1),
    # add custom player component
    player_comp := PlayerController(),
)

##### PORTAL #####

# Create animation for portal
flag_sheet = rb.Spritesheet(
    path="files/flag.png",
    sprite_size=rb.Vector(32, 32),
    grid_size=rb.Vector(6, 1),
)

flag_animation = rb.Animation(scale=rb.Vector(4, 4), fps=6)
flag_animation.add_spritesheet("", flag_sheet, to_coord=flag_sheet.end)

# create the end portal
flag = rb.GameObject()
flag.add(flag_animation)

flag.add(
    rb.Rectangle(
        trigger=True,
        tag="portal",
        width=flag_animation.anim_frame().size_scaled().x,
        height=flag_animation.anim_frame().size_scaled().y,
    )
)

##### SIDE BOUDARIES #####
left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))

##### LEVEL WIN TEXT #####
win_font = rb.Font(size=128, color=rb.Color.green.darker(75), styles=["bold"])
win_text = rb.GameObject(z_index=10000).add(rb.Text("YOU WIN!", win_font, anchor=(0, 0.5)))
win_sub_text = rb.GameObject(pos=(0, -100), z_index=10000).add(rb.Text("Click anywhere to move on", white_32))


##### CLOUD #####
class CloudMover(rb.Component):

    def __init__(self):
        super().__init__()
        self.speed = randint(10, 50)

    def update(self):
        if isinstance(scene := rb.Game.current(), DataScene):
            if self.gameobj.pos.x < -1100:
                self.gameobj.pos.x = scene.level_size - 860  # -960 + 100

        self.gameobj.pos += rb.Vector(-self.speed, 0) * rb.Time.delta_time

    def clone(self):
        return CloudMover()


cloud_template = rb.GameObject().add(rb.Image("files/cloud.png", scale=rb.Vector(2, 2)), CloudMover())


def cloud_generator(scene: DataScene, num_clouds: int, top_only: bool = False):
    half_width = int(rb.Display.res.x / 2)
    half_height = int(rb.Display.res.y / 2)

    for _ in range(num_clouds):
        rand_pos = rb.Vector(
            randint(-half_width, scene.level_size - half_width),
            randint(0 if top_only else -half_height, half_height),
        )

        cloud = cloud_template.clone()
        cloud.pos = rand_pos

        scene.add(cloud)


##### NICE BUTTON #####
def smooth_button_generator(pos, w, h, text, onrelease, color):
    t = rb.Text(text, white_32.clone())
    r = rb.Raster(w, h, z_index=-1)
    r.fill(color)

    b = rb.Button(
        w,
        h,
        onhover=lambda: rb.Time.recurrent_call(increase_font_size, 0.003),
        onexit=lambda: rb.Time.recurrent_call(decrease_font_size, 0.003),
        onrelease=onrelease,
    )

    font_changing: rb.RecurrentTask | None = None

    def increase_font_size(task: rb.RecurrentTask):
        nonlocal font_changing
        if font_changing is not None and font_changing != task:
            font_changing.stop()
        t.font_size += 1
        if t.font_size >= 64:
            task.stop()
            font_changing = None
            t.font_size = 64
        else:
            font_changing = task

    def decrease_font_size(task: rb.RecurrentTask):
        nonlocal font_changing
        if font_changing is not None and font_changing != task:
            font_changing.stop()
        t.font_size -= 1
        if t.font_size <= 32:
            task.stop()
            font_changing = None
            t.font_size = 32
        else:
            font_changing = task

    return rb.GameObject(pos=pos).add(b, t, r)
