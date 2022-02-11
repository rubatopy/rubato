"""
A module that houses all of the default options.
"""

from rubato.utils import Vector, Color, Polygon, Math, COL_TYPE

# [start-defaults]
game_defaults = {
    "name": "Untitled Game",
    "window_width": 600,
    "window_height": 400,
    "aspect_ratio": 1.5,
    "fps": 60,
    "reset_display": True,
    "better_clock": True,
}

rigidbody_defaults = {
    "mass": 1,
    "hitbox": Polygon.generate_polygon(4),
    "do_physics": True,
    "gravity": 100,
    "max_speed": Vector(Math.INFINITY, Math.INFINITY),
    "min_speed": Vector(-Math.INFINITY, -Math.INFINITY),
    "friction": Vector(1, 1),
    "col_type": COL_TYPE.STATIC,
    "scale": Vector(1, 1),
    "debug": False,
    "rotation": 0,
}

image_defaults = {
    "image_location": "default",  # str
    "scale_factor": Vector(1, 1),  # Vector
    "rotation": 0,  # float
}

sprite_defaults = {
    "pos": Vector(),  # Vector
    "z_index": 0,  # int
}

button_defaults = {
    "text": "default_text",
    "pos": Vector(),
    "size": 16,
    "z_index": 0,
    "font_name": "Arial",
    "color": Color.black,
}

rect_defaults = {
    "dims": Vector(),
    "color": Color.black,
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

animation_defaults = {
    "scale_factor": Vector(1, 1),
    "default_animation_length": 5,
    "rotation": 0,
}
# [end-defaults]


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
