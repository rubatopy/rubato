"""
A module that houses all of the default options.
"""
import sdl2, sdl2.sdlttf

from . import Math, Vector


class Defaults:
    """
    The default values for everything.
    """
    # [game]
    game_defaults = {
        "name": "Untitled Game",  # . . . . . . . . . . . . . . . . str
        # The title that appears at the top of the window
        "window_size": Vector(360, 360),  # . . . . . . . . . . . . Vector
        # The actual size of the window, cast to int Vector.
        "res": Vector(1080, 1080),  # . . . . . . . . . . . . . . . Vector
        # The pixel resolution of the game, cast to int Vector.
        "target_fps": 0,  # . . . . . . . . . . . . . . . . . . . . int
        # The target FPS of the game
        "physics_fps": 30,  # . . . . . . . . . . . . . . . . . . . int
        # The target physics FPS of the game
        "border_color": (0, 0, 0),  # . . . . . . . . . . . . . . . tuple or Color
        # The color of the borders
        "background_color": (255, 255, 255),  # . . . . . . . . . . tuple or Color
        # The background color of the window
        "icon": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
        # The path to an image to use as the window icon.
        "hidden": False,  #. . . . . . . . . . . . . . . . . . . bool
        # Whether the window is hidden. CANNOT BE CHANGED AFTER INIT CALL.
    }
    # [/game]
    # [group]
    group_defaults = {
        "name": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
        # The name of the game object. (Used in error messages)
        "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
        # The z_index of the group.
        "active": True,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether the group is drawn and updated.
    }
    # [/group]
    # [gameobj]
    gameobj_defaults = {
        "name": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
        # The name of the game object. (Used in error messages)
        "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
        # The starting position of the game object.
        "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
        # The z_index of the game object.
        "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether to draw a plus sign at the game object's position
        "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
        # The rotation of the game object in degrees.
    }
    # [/gameobj]
    # [ui]
    ui_defaults = {}
    # [/ui]
    # [component]
    component_defaults = {
        "offset": Vector(0, 0),  #. . . . . . . . . . . . . . . . . Vector
        # The offset from the center of the game object that the hitbox should be placed.
        "rot_offset": 0,  # . . . . . . . . . . . . . . . . . . . . float
        # The rotational offset. This is offset from the game object's rotation.
    }
    # [/component]
    # [text]
    text_defaults = {
        "text": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
        # The text to display.
        "justify": "left",  # . . . . . . . . . . . . . . . . . . . str
        # The justification of the text. (left, center, right)
        "anchor": Vector(),  # . . . . . . . . . . . . . . . . . . . str
        # The anchor position of the text. The zero vector means it is centered.
        # x component is whether to shift left, none, or right (-1, 0, 1)
        # y component is whether to shift top, none, or bottom (-1, 0, 1)
        "width": -1,  # . . . . . . . . . . . . . . . . . . . . . . int
        # The maximum width of the text. Will automatically wrap the text.
        "font": None,  #. . . . . . . . . . . . . . . . . . . . . . Font
        # The font object to use. Defaults to the default Font object (Font()).
    }
    # [/text]
    # [font]
    font_defaults = {
        "font": "Roboto",  #. . . . . . . . . . . . . . . . . . . . str
        # The name or path of the font to use.
        # Builtin fonts: Comfortaa, Fredoka, Merriweather, Roboto, SourceCodePro, PressStart
        "size": 16,  #. . . . . . . . . . . . . . . . . . . . . . . int
        # The size of the text.
        "styles": ["normal"],  # . . . . . . . . . . . . . . . . . . List[str]
        # A list containing the style to apply to the text. (bold, italic, underline, strikethrough)
        "color": (0, 0, 0, 255),  # . . . . . . . . . . . . . . . . tuple or Color
        # The color of the text.
    }
    # [/font]
    # [button]
    button_defaults = {
        "width": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
        # The width of the clickable area.
        "height": 10,  # . . . . . . . . . . . . . . . . . . . . . int
        # The height of the clickable area.
        "onclick": lambda: None,  #. . . . . . . . . . . . . . . . Callable
        # The callback to call when the button is clicked.
        "onrelease": lambda: None,  #. . . . . . . . . . . . . . . Callable
        # The callback to call when the button is released.
        "onhover": lambda: None,  #. . . . . . . . . . . . . . . . Callable
        # The callback to call when the mouse is hovering over the button.
        "onexit": lambda: None,  # . . . . . . . . . . . . . . . . Callable
        # The callback to call when the mouse stops hovering over the button.

    }
    # [/button]
    # [slider]
    slider_defaults = {
        "button_width": 10,  # . . . . . . . . . . . . . . . . . . int
        # The width of the clickable area.
        "button_height": 10,  #. . . . . . . . . . . . . . . . . . int
        # The height of the clickable area.
        "onclick": lambda: None,  #. . . . . . . . . . . . . . . . Callable
        # The callback to call when the button is clicked.
        "onrelease": lambda: None,  #. . . . . . . . . . . . . . . Callable
        # The callback to call when the button is released.
        "onhover": lambda: None,  #. . . . . . . . . . . . . . . . Callable
        # The callback to call when the mouse is hovering over the button.
        "onexit": lambda: None,  # . . . . . . . . . . . . . . . . Callable
        # The callback to call when the mouse stops hovering over the button.
        "slider_origin_offset": Vector(0, 0),  # . . . . . . . .  .Vector
        # The origin of the slider.
        "slider_length": 10,  # . . . . . . . . . . . . . . . . . .int
        # The length of the slider.
        "slider_direction": Vector(0, -1),  # . . . . . . . . . . .Vector
        # The direction of the slider.

    }
    # [/slider]
    # [rigidbody]
    rigidbody_defaults = {
        "density": 1,  #. . . . . . . . . . . . . . . . . . . . . . float
        # The density of the object. Will be used to automatically calculate mass and moment based on hitboxes.
        # (0 for infinite)
        "bounciness": 0,  # . . . . . . . . . . . . . . . . . . . . float
        # The percent bounciness of the RB. (as a decimal)
        "gravity": Vector(),  # . . . . . . . . . . . . . . . . . . Vector
        # The gravity applied to the RB.
        "max_speed": Vector(Math.INF, Math.INF),  # . . . . . . . . Vector
        # The maximum speed of the RB.
        "velocity": Vector(),  #. . . . . . . . . . . . . . . . . . Vector
        # The starting velocity of the RB.
        "friction": 0,  # . . . . . . . . . . . . . . . . . . . . . float
        # The amount of friction experienced by the RB.
        "static": False,  # . . . . . . . . . . . . . . . . . . . . bool
        # Whether the RB is static or not.
        "pos_correction": 0.25,  #. . . . . . . . . . . . . . . . . float
        # The amount of the collision to handle every fixed update. Set to 1.0 for platformers.
        "ang_vel": 0,  #. . . . . . . . . . . . . . . . . . . . . . bool
        # The starting angular velocity of the RB.
        "moment": -1,  #. . . . . . . . . . . . . . . . . . . . . . float
        # The moment of inertia of the RB. WILL OVERRIDE DENSITY IF SET. (0 for infinite)
        # If moment is set, mass must also be set.
        "mass": -1,  #. . . . . . . . . . . . . . . . . . . . . . . float
        # The mass of the RB. WILL OVERRIDE DENSITY IF SET. (0 for infinite)
        # If mass is set, moment must also be set.
        "advanced": False,  # . . . . . . . . . . . . . . . . . . . bool
        # The type of collision resolution algorithm. If True, rotational resolution will be enabled.
    }
    # [/rigidbody]
    # [image]
    image_defaults = {
        "rel_path": "",  #. . . . . . . . . . . . . . . . . . . . . str
        # The relative path of the image. (from the cwd)
        "size": Vector(32, 32),  #. . . . . . . . . . . . . . . . . Vector
        # The size of the image in pixels. (if a rel path is set this value will be ignored)
        "scale": Vector(1, 1),  # . . . . . . . . . . . . . . . . . Vector
        # The initial scale factor of the image.
        "anti_aliasing": False,  #. . . . . . . . . . . . . . . . . bool
        # Whether or not to enable anti aliasing.
        "flipx": False,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not to flip the image along the x axis
        "flipy": False,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not to flip the image along the y axis
        "visible": True,  # . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not the image is visible.
    }
    # [/image]
    # [raster]
    raster_defaults = {
        "width": 32,  # . . . . . . . . . . . . . . . . . . . . . . int
        # The number of pixels wide the raster is.
        "height": 32,  #. . . . . . . . . . . . . . . . . . . . . . int
        # The number of pixels tall the raster is.
        "scale": Vector(1, 1),  # . . . . . . . . . . . . . . . . . Vector
        # The amount to scale the raster by.
        "visible": True,  # . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not the raster is visible.
    }
    # [/raster]
    # [animation]
    animation_defaults = {
        "scale": Vector(1, 1),  # . . . . . . . . . . . . . . . . . Vector
        # The startin scale factor of the animation.
        "fps": 24,  # . . . . . . . . . . . . . . . . . . . . . . . int
        # The FPS that the animation should run at. Greater than 0.
        "anti_aliasing": False,  #. . . . . . . . . . . . . . . . . bool
        # Whether or not to enable anti aliasing.
        "flipx": False,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not to flip the animation along the x axis
        "flipy": False,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not to flip the animation along the y axis
        "visible": True,  # . . . . . . . . . . . . . . . . . . . . bool
        # Whether or not the image is visible.
    }
    # [/animation]
    # [spritesheet]
    spritesheet_defaults = {
        "rel_path": "",  #. . . . . . . . . . . . . . . . . . . . . str
        # The relative path to the spritesheet (from the cwd).
        "sprite_size": Vector(32, 32),  # . . . . . . . . . . . . . Vector
        # The size of each sprite in pixels.
        "grid_size": None,  # . . . . . . . . . . . . . . Vector
        # The size of the spritesheet grid (columns/x, rows/y).
    }
    # [/spritesheet]
    # [hitbox]
    hitbox_defaults = {
        "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
        # Whether to draw a green outline around the Polygon or not.
        "trigger": False,  #. . . . . . . . . . . . . . . . . . . . bool
        # Whether this hitbox is just a trigger or not.
        "scale": 1,  #. . . . . . . . . . . . . . . . . . . . . . . int
        # The scale of the polygon
        "on_collide": lambda Manifold: None,  #. . . . . . . . . . . Callable
        # The on_collide function to call when a collision happens with this hitbox
        # Must take a rb.Manifold.
        "on_exit": lambda Manifold: None,  # . . . . . . . . . . . . Callable
        # The on_exit function to call when a collision ends with this hitbox.
        # Must take a rb.Manifold.
        "color": None,  # . . . . . . . . . . . . . . . . . . . . . Color
        # The color to fill this hitbox with.
        "tag": "",  # . . . . . . . . . . . . . . . . . . . . . . . str
        # The tag of the hitbox (can be used to identify hitboxes)
    }
    # [/hitbox]
    # [polygon]
    polygon_defaults = {
        "verts": [],  # . . . . . . . . . . . . . . . . . . . . . . List[Vector]
        # A list of vectors representing the vertices of the Polygon going CCW.
    }
    # [/polygon]
    # [rectangle]
    rectangle_defaults = {
        "width": 10,  # . . . . . . . . . . . . . . . . . . . . . . int
        # The width of the rectangle.
        "height": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
        # The height of the rectangle.
    }
    # [/rectangle]
    # [circle]
    circle_defaults = {
        "radius": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
        # The radius of the circle.
    }
    # [/circle]
    # [color]
    color_defaults = {
        "yellow": (253, 203, 110),  # . . . . . . . . . . . . . . . tuple
        "scarlet": (214, 48, 49),  #. . . . . . . . . . . . . . . . tuple
        "violet": (108, 92, 231),  #. . . . . . . . . . . . . . . . tuple
        "turquoize": (0, 206, 201),  #. . . . . . . . . . . . . . . tuple
        "orange": (225, 112, 85),  #. . . . . . . . . . . . . . . . tuple
        "magenta": (232, 67, 147),  # . . . . . . . . . . . . . . . tuple
        "blue": (9, 132, 227),  # . . . . . . . . . . . . . . . . . tuple
        "green": (0, 184, 148),  #. . . . . . . . . . . . . . . . . tuple
        "red": (255, 118, 117),  #. . . . . . . . . . . . . . . . . tuple
        "purple": (162, 155, 254),  # . . . . . . . . . . . . . . . tuple
        "cyan": (116, 185, 255),  # . . . . . . . . . . . . . . . . tuple
        "lime": (85, 239, 196),  #. . . . . . . . . . . . . . . . . tuple

        # colorwheel used (rgb values are not identical):
        # https://upload.wikimedia.org/wikipedia/commons/5/54/RGV_color_wheel_1908.png
    }
    # [/color]
    # [grayscale]
    grayscale_defaults = {
        "black": (0, 0, 0),  #. . . . . . . . . . . . . . . . . . . tuple
        "white": (255, 255, 255),  #. . . . . . . . . . . . . . . . tuple
        "night": (20, 20, 22),  # . . . . . . . . . . . . . . . . . tuple
        "darkgray": (45, 52, 54),  #. . . . . . . . . . . . . . . . tuple
        "gray": (99, 110, 114),  #. . . . . . . . . . . . . . . . . tuple
        "lightgray": (178, 190, 195),  #. . . . . . . . . . . . . . tuple
        "snow": (223, 230, 233),  # . . . . . . . . . . . . . . . . tuple
    }
    # [/grayscale]

    text_fonts = {
        "Comfortaa": "Comfortaa-Regular.ttf",
        "Fredoka": "Fredoka-Regular.ttf",
        "Merriweather": "Merriweather-Regular.ttf",
        "Roboto": "Roboto-Regular.ttf",
        "SourceCodePro": "SourceCodePro-Regular.ttf",
        "PressStart": "PressStart2P-Regular.ttf",
    }

    text_styles = {
        "bold": sdl2.sdlttf.TTF_STYLE_BOLD,
        "italic": sdl2.sdlttf.TTF_STYLE_ITALIC,
        "underline": sdl2.sdlttf.TTF_STYLE_UNDERLINE,
        "strikethrough": sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH,
        "normal": sdl2.sdlttf.TTF_STYLE_NORMAL,
    }


def check_locals(locals_dict):
    """
    Checks wether we should use the options or the locals.
    """
    if bool(locals_dict["options"]):
        return locals_dict["options"]
    # use options
    else:
        locals_dict.pop("options")
        return locals_dict
