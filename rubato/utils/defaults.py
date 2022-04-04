"""
A module that houses all of the default options.
"""
import sdl2, sdl2.sdlttf

from . import Math, Vector

# [start-defaults]
game_defaults = {
    "name": "Untitled Game",  # . . . . . . . . . . . . . . . . str
    # The title that appears at the top of the window
    "window_size": Vector(360, 360),  # . . . . . . . . . . . . Vector
    # The actual size of the window
    "res": Vector(1080, 1080),  # . . . . . . . . . . . . . . . Vector
    # The pixel resolution of the game
    "target_fps": 0,  # . . . . . . . . . . . . . . . . . . . . int
    # The target FPS of the game
    "physics_fps": 60,  # . . . . . . . . . . . . . . . . . . . int
    # The target physics FPS of the game
    "border_color": (0, 0, 0),  # . . . . . . . . . . . . . . . tuple or Color
    # The color of the borders
    "background_color": (255, 255, 255),  # . . . . . . . . . . tuple or Color
    # The background color of the window
    "icon": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The path to an image to use as the window icon.
}

group_defaults = {
    "name": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The name of the game object. (Used in error messages)
    "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The z_index of the group.
}

ui_defaults = {  # Can also contain elements from the game object defaults
}

gameobj_defaults = {
    "name": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The name of the game object. (Used in error messages)
    "pos": Vector(),  # . . . . . . . . . . . . . . . . . . . . Vector
    # The starting position of the game object.
    "z_index": 0,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The z_index of the game object.
    "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether to draw a plus sign at the game object's position
}

text_defaults = {
    "text": "",  #. . . . . . . . . . . . . . . . . . . . . . . str
    # The text to display.
    "justify": "left",  # . . . . . . . . . . . . . . . . . . . str
    # The justification of the text. (left, center, right)
    "align": Vector(),  # . . . . . . . . . . . . . . . . . . . str
    # The alignment of the text. The zero vector means it is centered.
    # x component is whether to shift left, none, or right (-1, 0, 1)
    # y component is whether to shift top, none, or bottom (-1, 0, 1)
    "width": -1,  # . . . . . . . . . . . . . . . . . . . . . . int
    # The maximum width of the text. Will automatically wrap the text.
}

font_defaults = {
    "font": "Roboto",  #. . . . . . . . . . . . . . . . . . . . str
    # The name or path of the font to use.
    "size": 16,  #. . . . . . . . . . . . . . . . . . . . . . . int
    # The size of the text.
    "styles": ["normal"],  # . . . . . . . . . . . . . . . . . . List[str]
    # A list containing the style to apply to the text. (bold, italic, underline, strikethrough)
    "color": (0, 0, 0, 255),  # . . . . . . . . . . . . . . . . tuple or Color
    # The color of the text.
}

rigidbody_defaults = {
    "mass": 1,  # . . . . . . . . . . . . . . . . . . . . . . . float
    # The mass of the RB. (0 for infinite)
    "bounciness": 0,  # . . . . . . . . . . . . . . . . . . . . float
    # The percent bounciness of the RB. (as a decimal)
    "gravity": Vector(0, 100),  # . . . . . . . . . . . . . . . Vector
    # The gravity applied to the RB.
    "max_speed": Vector(Math.INF, Math.INF),  # . . . . . . . . Vector
    # The maximum speed of the RB.
    "velocity": Vector(),  #. . . . . . . . . . . . . . . . . . Vector
    # The starting velocity of the RB.
    "friction": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The amount of friction experienced by the RB.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The starting rotation of the RB.
    "static": False,  # . . . . . . . . . . . . . . . . . . . . bool
    # Whether the RB is static or not.
    "pos_correction": 0.25,  #. . . . . . . . . . . . . . . . . float
}

image_defaults = {
    "rel_path": "",  #. . . . . . . . . . . . . . . . . . . . . str
    # The relative path of the image. (from the cwd)
    "size": Vector(32, 32),  #. . . . . . . . . . . . . . . . . Vector
    # The size of the image in pixels. (if a rel path is set this value will be ignored)
    "scale": Vector(1, 1),  # . . . . . . . . . . . . . . . . . Vector
    # The initial scale factor of the image.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The initial rotation of the image.
    "anti_aliasing": False,  #. . . . . . . . . . . . . . . . . bool
    # Whether or not to enable anti aliasing.
    "flipx": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether or not to flip the image along the x axis
    "flipy": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether or not to flip the image along the y axis
    "offset": Vector(0, 0),  #. . . . . . . . . . . . . . . . . Vector
    # The offset from the center of the game object that the hitbox should be placed.
    "visible": True,  # . . . . . . . . . . . . . . . . . . . . bool
    # Whether or not the image is visible.
}

animation_defaults = {
    "scale": Vector(1, 1),  # . . . . . . . . . . . . . . . . . Vector
    # The startin scale factor of the animation.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the animation.
    "fps": 24,  # . . . . . . . . . . . . . . . . . . . . . . . int
    # The FPS that the animation should run at. Greater than 0.
    "anti_aliasing": False,  #. . . . . . . . . . . . . . . . . bool
    # Whether or not to enable anti aliasing.
    "flipx": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether or not to flip the animation along the x axis
    "flipy": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether or not to flip the animation along the y axis
    "offset": Vector(0, 0),  #. . . . . . . . . . . . . . . . . Vector
    # The offset from the center of the game object that the hitbox should be placed.
    "visible": True,  # . . . . . . . . . . . . . . . . . . . . bool
    # Whether or not the image is visible.
}

spritesheet_defaults = {
    "rel_path": "",  #. . . . . . . . . . . . . . . . . . . . . str
    # The relative path to the spritesheet (from the cwd).
    "sprite_size": Vector(32, 32),  # . . . . . . . . . . . . . Vector
    # The size of each sprite in pixels.
    "grid_size": None,  # . . . . . . . . . . . . . . Vector
    # The size of the spritesheet grid (columns/x, rows/y).
}

hitbox_defaults = {
    "debug": False,  #. . . . . . . . . . . . . . . . . . . . . bool
    # Whether to draw a green outline around the Polygon or not.
    "trigger": False,  #. . . . . . . . . . . . . . . . . . . . bool
    # Whether this hitbox is just a trigger or not.
    "scale": 1,  #. . . . . . . . . . . . . . . . . . . . . . . int
    # The scale of the polygon
    "on_collide": lambda colInfo: None,  #. . . . . . . . . . . Callable
    # The on_collide function to call when a collision happens with this hitbox
    # Must take a rb.ColInfo.
    "color": None,  # . . . . . . . . . . . . . . . . . . . . . Color
    # The color to fill this hitbox with.
    "tag": "",  # . . . . . . . . . . . . . . . . . . . . . . . str
    # The tag of the hitbox (can be used to identify hitboxes)
    "offset": Vector(0, 0),  #. . . . . . . . . . . . . . . . . Vector
    # The offset from the center of the game object that the hitbox should be placed.
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
    "height": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The height of the rectangle.
    "rotation": 0,  # . . . . . . . . . . . . . . . . . . . . . float
    # The rotation of the rectangle
}

circle_defaults = {  # Can also contain elements from the hitbox defaults
    "radius": 10,  #. . . . . . . . . . . . . . . . . . . . . . int
    # The radius of the circle.
}

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

grayscale_defaults = {
    "black": (0, 0, 0),  #. . . . . . . . . . . . . . . . . . . tuple
    "white": (255, 255, 255),  #. . . . . . . . . . . . . . . . tuple
    "night": (20, 20, 22),  # . . . . . . . . . . . . . . . . . tuple
    "darkgray": (45, 52, 54),  #. . . . . . . . . . . . . . . . tuple
    "gray": (99, 110, 114),  #. . . . . . . . . . . . . . . . . tuple
    "lightgray": (178, 190, 195),  #. . . . . . . . . . . . . . tuple
    "snow": (223, 230, 233),  # . . . . . . . . . . . . . . . . tuple
}
# [end-defaults]

text_fonts = {
    "Comfortaa": "static/fonts/Comfortaa-Regular.ttf",
    "Fredoka": "static/fonts/Fredoka-Regular.ttf",
    "Merriweather": "static/fonts/Merriweather-Regular.ttf",
    "Roboto": "static/fonts/Roboto-Regular.ttf",
    "SourceCodePro": "static/fonts/SourceCodePro-Regular.ttf",
    "PressStart": "static/fonts/PressStart2P-Regular.ttf",
}

text_styles = {
    "bold": sdl2.sdlttf.TTF_STYLE_BOLD,
    "italic": sdl2.sdlttf.TTF_STYLE_ITALIC,
    "underline": sdl2.sdlttf.TTF_STYLE_UNDERLINE,
    "strikethrough": sdl2.sdlttf.TTF_STYLE_STRIKETHROUGH,
    "normal": sdl2.sdlttf.TTF_STYLE_NORMAL,
}


class Defaults:
    """
    The default values for everything.
    """
    game_defaults = game_defaults
    group_defaults = group_defaults
    ui_defaults = ui_defaults
    gameobj_defaults = gameobj_defaults
    text_defaults = text_defaults
    font_defaults = font_defaults
    rigidbody_defaults = rigidbody_defaults
    image_defaults = image_defaults
    animation_defaults = animation_defaults
    spritesheet_defaults = spritesheet_defaults
    hitbox_defaults = hitbox_defaults
    polygon_defaults = polygon_defaults
    rectangle_defaults = rectangle_defaults
    circle_defaults = circle_defaults
    color_defaults = color_defaults
    grayscale_defaults = grayscale_defaults
    text_fonts = text_fonts
    text_styles = text_styles
