"""
A module that houses all of the default options.
"""

from rubato.utils import Math, Vector, Color

# [start-defaults]
game_defaults = {
    "name": "Untitled Game",  # . . . . . . . . . . . . . . . . str
    "window_width": 600,  # . . . . . . . . . . . . . . . . . . int
    "window_height": 400,  #. . . . . . . . . . . . . . . . . . int
    "aspect_ratio": 1.5,  # . . . . . . . . . . . . . . . . . . float
    "fps_cap": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    "physics_timestep": 20,  #. . . . . . . . . . . . . . . . . int
    "reset_display": True,  # . . . . . . . . . . . . . . . . . bool
    "better_clock": True,  #. . . . . . . . . . . . . . . . . . bool
}

rigidbody_defaults = {
    "mass": 1,  # . . . . . . . . . . . . . . . . . . . . . . . float
    "bouncyness": 0,  # . . . . . . . . . . . . . . . . . . . . float
    "gravity": Vector(0, 100),  # . . . . . . . . . . . . . . . Vector
    "max_speed": Vector(Math.INFINITY, Math.INFINITY),  # . . . Vector
    "min_speed": Vector(-Math.INFINITY, -Math.INFINITY),  # . . Vector
    "friction": 0.9,  # . . . . . . . . . . . . . . . . . . . . float
    "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    "static": False  #. . . . . . . . . . . . . . . . . . . . . bool
}

image_defaults = {
    "image_location": "default",  # . . . . . . . . . . . . . . str
    "scale_factor": Vector(1, 1),  #. . . . . . . . . . . . . . Vector
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
}

sprite_defaults = {
    "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
    "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
}

rect_defaults = {
    "dims": Vector(),  #. . . . . . . . . . . . . . . . . . . . Vector
    "color": Color.black,  #. . . . . . . . . . . . . . . . . . Color
}

animation_defaults = {
    "scale_factor": Vector(1, 1),  #. . . . . . . . . . . . . . Vector
    "default_animation_length": 5,  # . . . . . . . . . . . . . int
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    "fps": 24,  # . . . . . . . . . . . . . . . . . . . . . . . int
}
# [end-defaults]

button_defaults = {
    "text": "default_text",  #. . . . . . . . . . . . . . . . . str
    "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
    "size": 16,  #. . . . . . . . . . . . . . . . . . . . . . . int
    "z_index": 0,  #
    "font_name": "Arial",  #
    "color": Color.black,  #
}

text_defaults = {
    "text": "default_text",
    "pos": Vector(),
    "size": 16,
    "z_index": 0,
    "font_name": "Arial",
    "color": Color.black,
    "static": False,
    "onto_surface": None,
}


def merge_params(options: dict, defaults: dict) -> dict:
    """
    Merges an incomplete options dictionary with the defaults dictionary

    Args:
        options: The incomplete options dictionary
        defaults: The default dictionary

    Returns:
        dict: The merged dictionary
    """
    merged = {}
    keys = defaults.keys()

    for key in keys:
        merged[key] = options.get(key, defaults[key])

    return merged
