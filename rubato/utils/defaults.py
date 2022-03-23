"""
A module that houses all of the default options.
"""

from rubato.utils import Math, Vector

# [start-defaults]
game_defaults = {
    "name": "Untitled Game",  # . . . . . . . . . . . . . . . . str
    # The title that appears at the top of the window
    "window_size": Vector(360, 360),  # . . . . . . . . . . . . Vector
    # The actual size of the window
    "resolution": Vector(1080, 1080),  #. . . . . . . . . . . . Vector
    # The pixel resolution of the game
    "target_fps": 0,  # . . . . . . . . . . . . . . . . . . . . int
    # The target FPS of the game
    "physics_fps": 60,  # . . . . . . . . . . . . . . . . . . . int
    # The target physics FPS of the game
    "background_color": (0, 0, 0),  # . . . . . . . . . . . . . tuple or Color
    # The background color of the window. (Usually the borders)
    "foreground_color": (255, 255, 255),  # . . . . . . . . . . tuple or Color
    # The foreground color of the window.
    # (i.e. the background of the main game).
    "icon": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The path to an image to use as the window icon.
}

rigidbody_defaults = {
    "mass": 1,  # . . . . . . . . . . . . . . . . . . . . . . . float
    # The mass of the RB. (0 for infinite)
    "bounciness": 0,  # . . . . . . . . . . . . . . . . . . . . float
    # The percent bounciness of the RB. (as a decimal)
    "gravity": Vector(0, 100),  # . . . . . . . . . . . . . . . Vector
    # The gravity applied to the RB.
    "max_speed": Vector(Math.INFINITY, Math.INFINITY),  # . . . Vector
    # The maximum speed of the RB.
    "velocity": Vector(),  #. . . . . . . . . . . . . . . . . . Vector
    # The starting velocity of the RB.
    "friction": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The amount of friction experienced by the RB.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The starting rotation of the RB.
    "static": False,  # . . . . . . . . . . . . . . . . . . . . bool
    # Whether the RB is static or not.
}

image_defaults = {
    "image_location": "",  #. . . . . . . . . . . . . . . . . . str
    # The relative path of the image. (from the cwd)
    "scale_factor": Vector(1, 1),  #. . . . . . . . . . . . . . Vector
    # The initial scale factor of the image.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The initial rotation of the image.
}

sprite_defaults = {
    "name": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The name of the sprite. (Used in error messages)
    "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
    # The starting position of the sprite.
    "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The z_index of the sprite.
    "debug": False,  # . . . . . . . . . . . . . . . . . . . . . bool
    # Whether to draw a plus sign at the sprite's position
}

group_defaults = {
    "name": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The name of the sprite. (Used in error messages)
    "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The z_index of the group.
}

animation_defaults = {
    "scale_factor": Vector(1, 1),  #. . . . . . . . . . . . . . Vector
    # The startin scale factor of the animation.
    "default_animation_length": 5,  # . . . . . . . . . . . . . int
    # The default number of frames in the animation.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the animation.
    "fps": 24,  # . . . . . . . . . . . . . . . . . . . . . . . int
    # The FPS that the animation should run at.
}

hitbox_defaults = {
    "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether to draw a green outline around the Polygon or not.
    "trigger": False,  #. . . . . . . . . . . . . . . . . . . . bool
    # Whether this hitbox is just a trigger or not.
    "scale": 1,  #. . . . . . . . . . . . . . . . . . . . . . . int
    # The scale of the polygon
    "on_collide": lambda c: None,  #. . . . . . . . . . . . . . . Callable
    # The on_collide function to call when a collision happens with this hitbox.
    "color": None,  # . . . . . . . . . . . . . . . . . . . . . Color
    # The color to fill this hitbox with.
}

polygon_defaults = {  # Can also contain elements from the hitbox defaults
    "verts": [],  # . . . . . . . . . . . . . . . . . . . . . . List[Vector]
    # A list of vectors representing the vertices of the Polygon going CCW.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the polygon
}

rectangle_defaults = {  # Can also contain elements from the hitbox defaults
    "width": 10,  # . . . . . . . . . . . . . . . . . . . . . . int
    # The width of the rectangle.
    "height": 10,  # . . . . . . . . . . . . . . . . . . . . . . int
    # The height of the rectangle.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the rectangle
}

circle_defaults = {  # Can also contain elements from the hitbox defaults
    "radius": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The radius of the circle.
}

color_defaults = {
    "yellow": (253, 203, 110),  #. . . . . . . . . . . . . . . . tuple
    "scarlet": (214, 48, 49),  # . . . . . . . . . . . . . . . . tuple
    "violet": (108, 92, 231),  # . . . . . . . . . . . . . . . . tuple
    "turquoize": (0, 206, 201),  # . . . . . . . . . . . . . . . tuple
    "orange": (225, 112, 85),  # . . . . . . . . . . . . . . . . tuple
    "magenta": (232, 67, 147),  #. . . . . . . . . . . . . . . . tuple
    "blue": (9, 132, 227),  #. . . . . . . . . . . . . . . . . . tuple
    "green": (0, 184, 148),  # . . . . . . . . . . . . . . . . . tuple
    "red": (255, 118, 117),  # . . . . . . . . . . . . . . . . . tuple
    "purple": (162, 155, 254),  #. . . . . . . . . . . . . . . . tuple
    "cyan": (116, 185, 255),  #. . . . . . . . . . . . . . . . . tuple
    "lime": (85, 239, 196),  # . . . . . . . . . . . . . . . . . tuple

    # colorwheel used (rgb values are not identical):
    # https://upload.wikimedia.org/wikipedia/commons/5/54/RGV_color_wheel_1908.png
}

grayscale_defaults = {
    "black": (0, 0, 0),  # . . . . . . . . . . . . . . . . . . . tuple
    "white": (255, 255, 255),  # . . . . . . . . . . . . . . . . tuple
    "darkgray": (45, 52, 54),  # . . . . . . . . . . . . . . . . tuple
    "gray": (99, 110, 114),  # . . . . . . . . . . . . . . . . . tuple
    "lightgray": (178, 190, 195),  # . . . . . . . . . . . . . . tuple
    "snow": (223, 230, 233),  #. . . . . . . . . . . . . . . . . tuple
}

# [end-defaults]
