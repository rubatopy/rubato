from pygame import key, mouse
from pgp.utils import ClassProperty

class Input:
    """
    An abstraction of the PyGame input system. Slightly optimized and plays nice with the rest of pgp.
    """
    key = key
    mouse = mouse

    @staticmethod
    def is_pressed(char: str):
        return Input.key.get_pressed()[Input.key.key_code(char)]

    @ClassProperty
    def keys(self):
        return ['K_BACKSPACE', 'K_TAB', 'K_CLEAR', 'K_RETURN', 'K_PAUSE', 'K_ESCAPE', 'K_SPACE', 'K_EXCLAIM', 'K_QUOTEDBL',
         'K_HASH', 'K_DOLLAR', 'K_AMPERSAND', 'K_QUOTE', 'K_LEFTPAREN', 'K_RIGHTPAREN', 'K_ASTERISK', 'K_PLUS',
         'K_COMMA', 'K_MINUS', 'K_PERIOD', 'K_SLASH', 'K_0', 'K_1', 'K_2', 'K_3', 'K_4', 'K_5', 'K_6', 'K_7', 'K_8',
         'K_9', 'K_COLON', 'K_SEMICOLON', 'K_LESS', 'K_EQUALS', 'K_GREATER', 'K_QUESTION', 'K_AT', 'K_LEFTBRACKET',
         'K_BACKSLASH', 'K_RIGHTBRACKET', 'K_CARET', 'K_UNDERSCORE', 'K_BACKQUOTE', 'K_a', 'K_b', 'K_c', 'K_d', 'K_e',
         'K_f', 'K_g', 'K_h', 'K_i', 'K_j', 'K_k', 'K_l', 'K_m', 'K_n', 'K_o', 'K_p', 'K_q', 'K_r', 'K_s', 'K_t', 'K_u',
         'K_v', 'K_w', 'K_x', 'K_y', 'K_z', 'K_DELETE', 'K_KP0', 'K_KP1', 'K_KP2', 'K_KP3', 'K_KP4', 'K_KP5', 'K_KP6',
         'K_KP7', 'K_KP8', 'K_KP9', 'K_KP_PERIOD', 'K_KP_DIVIDE', 'K_KP_MULTIPLY', 'K_KP_MINUS', 'K_KP_PLUS',
         'K_KP_ENTER', 'K_KP_EQUALS', 'K_UP', 'K_DOWN', 'K_RIGHT', 'K_LEFT', 'K_INSERT', 'K_HOME', 'K_END', 'K_PAGEUP',
         'K_PAGEDOWN', 'K_F1', 'K_F2', 'K_F3', 'K_F4', 'K_F5', 'K_F6', 'K_F7', 'K_F8', 'K_F9', 'K_F10', 'K_F11',
         'K_F12', 'K_F13', 'K_F14', 'K_F15', 'K_NUMLOCK', 'K_CAPSLOCK', 'K_SCROLLOCK', 'K_RSHIFT', 'K_LSHIFT',
         'K_RCTRL', 'K_LCTRL', 'K_RALT', 'K_LALT', 'K_RMETA', 'K_LMETA', 'K_LSUPER', 'K_RSUPER', 'K_MODE', 'K_HELP',
         'K_PRINT', 'K_SYSREQ', 'K_BREAK', 'K_MENU', 'K_POWER', 'K_EURO']
