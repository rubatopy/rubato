import rubato as rb
from random import randint


##### DATA SCENE #####
class DataScene(rb.Scene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_size = 0


from player_controller import PlayerController

##### MISC #####

white_32 = rb.Font(size=32, color=rb.Color.white)
start_time = 0

##### COLORS #####

platform_color = rb.Color.from_hex("#b8e994")
background_color = rb.Color.from_hex("#82ccdd")
win_color = rb.Color.green.darker(75)

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

##### Flag #####

# Create animation for flag
flag_sheet = rb.Spritesheet(
    path="files/flag.png",
    sprite_size=rb.Vector(32, 32),
    grid_size=rb.Vector(6, 1),
)

flag_animation = rb.Animation(scale=rb.Vector(4, 4), fps=6, flipx=True)
flag_animation.add_spritesheet("", flag_sheet, to_coord=flag_sheet.end)

# create the end flag
flag = rb.GameObject()
flag.add(flag_animation)

flag.add(
    rb.Rectangle(
        trigger=True,
        tag="flag",
        width=-flag_animation.anim_frame().size_scaled().x,
        height=flag_animation.anim_frame().size_scaled().y,
    )
)

##### SIDE BOUDARIES #####
left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))

##### LEVEL WIN TEXT #####
win_font = rb.Font(size=128, color=win_color, styles=["bold"])
win_text = rb.GameObject(z_index=10000).add(rb.Text("YOU WIN!", win_font, anchor=(0, 0.5)))
