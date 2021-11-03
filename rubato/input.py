from pygame import key, mouse
from rubato.utils import classproperty, Vector


class Input:
    """
    An abstraction of the PyGame input system. Slightly optimized and plays nice with the rest of rubato.
    """
    key = key
    mouse = mouse

    @staticmethod
    def is_pressed(char: str) -> bool:
        return Input.key.get_pressed()[Input.key.key_code(char)]

    @staticmethod
    def mouse_over(center: Vector, dims: Vector = Vector(1,1)) -> bool:
        """
        Returns if the mouse is inside a rectangle defined by its center and dimensions.

        :param center: The center of the rectangle
        :param dims: The dimensions of the rectangle (Defaulted to 1 pixel if you need to check if the mouse is over a specific coord)
        """
        top_left = (center-dims/2).ceil()
        bottom_right = (center+dims/2).ceil()
        mouse_pos = Vector(Input.mouse.get_pos()[0], Input.mouse.get_pos()[1])

        return top_left.x <= mouse_pos.x <= bottom_right.x and top_left.y <= mouse_pos.y <= bottom_right.y

    @classproperty
    def KEYS(self):
        return ['BACKSPACE', 'TAB', 'CLEAR', 'RETURN', 'PAUSE', 'ESCAPE', 'SPACE', 'EXCLAIM', 'QUOTEDBL',
         'HASH', 'DOLLAR', 'AMPERSAND', 'QUOTE', 'LEFTPAREN', 'RIGHTPAREN', 'ASTERISK', 'PLUS',
         'COMMA', 'MINUS', 'PERIOD', 'SLASH', '0', '1', '2', '3', '4', '5', '6', '7', '8',
         '9', 'COLON', 'SEMICOLON', 'LESS', 'EQUALS', 'GREATER', 'QUESTION', 'AT', 'LEFTBRACKET',
         'BACKSLASH', 'RIGHTBRACKET', 'CARET', 'UNDERSCORE', 'BACKQUOTE', 'a', 'b', 'c', 'd', 'e',
         'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
         'v', 'w', 'x', 'y', 'z', 'DELETE', 'KP0', 'KP1', 'KP2', 'KP3', 'KP4', 'KP5', 'KP6',
         'KP7', 'KP8', 'KP9', 'KP_PERIOD', 'KP_DIVIDE', 'KP_MULTIPLY', 'KP_MINUS', 'KP_PLUS',
         'KP_ENTER', 'KP_EQUALS', 'UP', 'DOWN', 'RIGHT', 'LEFT', 'INSERT', 'HOME', 'END', 'PAGEUP',
         'PAGEDOWN', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
         'F12', 'F13', 'F14', 'F15', 'NUMLOCK', 'CAPSLOCK', 'SCROLLOCK', 'RSHIFT', 'LSHIFT',
         'RCTRL', 'LCTRL', 'RALT', 'LALT', 'RMETA', 'LMETA', 'LSUPER', 'RSUPER', 'MODE', 'HELP',
         'PRINT', 'SYSREQ', 'BREAK', 'MENU', 'POWER', 'EURO']
