import rubato as rb
from data_scene import DataScene
from player_controller import PlayerController
from random import randint

black_32 = rb.Font(size=32)
start_time = 0

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
all_portal_images = rb.Spritesheet(
    path="files/portals/portal1_spritesheet.png",
    sprite_size=rb.Vector(32, 32),
    grid_size=rb.Vector(8, 1),
)

portal_animation = rb.Animation(scale=rb.Vector(4, 4), fps=10)
portal_animation.add_spritesheet("", all_portal_images, to_coord=all_portal_images.end)

# create the end portal
end = rb.GameObject()
end.add(portal_animation)

end.add(
    rb.Rectangle(
        trigger=True,
        tag="portal",
        width=portal_animation.anim_frame().size_scaled().x,
        height=portal_animation.anim_frame().size_scaled().y,
    )
)

##### SIDE BOUDARIES #####
left = rb.GameObject(pos=rb.Display.center_left - rb.Vector(25, 0)).add(rb.Rectangle(width=50, height=rb.Display.res.y))
right = rb.GameObject().add(rb.Rectangle(width=50, height=rb.Display.res.y))

##### LEVEL WIN TEXT #####
win_font = rb.Font(size=128, color=rb.Color.green.darker(75), styles=["bold"])
win_text = rb.GameObject(z_index=2).add(rb.Text("YOU WIN!", win_font, anchor=(0, 0.5)))
win_sub_text = rb.GameObject(pos=(0, -100), z_index=2).add(rb.Text("Click anywhere to move on", black_32))

##### CLOUD #####
cloud_template = rb.GameObject().add(cloud_r := rb.Raster(300, 200))
cloud_r.draw_circle((-75, -25), 49, fill=rb.Color.white)
cloud_r.draw_circle((0, -25), 49, fill=rb.Color.white)
cloud_r.draw_circle((75, -25), 49, fill=rb.Color.white)
cloud_r.draw_circle((-37, 25), 49, fill=rb.Color.white)
cloud_r.draw_circle((37, 25), 49, fill=rb.Color.white)


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
    t = rb.Text(text, black_32.clone())
    r = rb.Raster(w, h, z_index=-1)
    r.fill(color)

    b = rb.Button(
        w,
        h,
        onhover=lambda: rb.Time.recurrent_call(increase_font_size, 3),
        onexit=lambda: rb.Time.recurrent_call(decrease_font_size, 3),
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
