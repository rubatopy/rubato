"""
The Input module is the way you collect input from the user.
"""
import ctypes
from typing import Tuple
import sdl2
from ctypes import c_char_p, c_long, c_int
from rubato.utils import Vector, Display

# KEYBOARD FUNCTIONS

_mods = {
    "shift": sdl2.KMOD_SHIFT,
    "left shift": sdl2.KMOD_LSHIFT,
    "right shift": sdl2.KMOD_RSHIFT,
    "alt": sdl2.KMOD_ALT,
    "left alt": sdl2.KMOD_LALT,
    "right alt": sdl2.KMOD_RALT,
    "ctrl": sdl2.KMOD_CTRL,
    "left ctrl": sdl2.KMOD_LCTRL,
    "right ctrl": sdl2.KMOD_RCTRL,
    "gui": sdl2.KMOD_GUI,
    "left gui": sdl2.KMOD_LGUI,
    "right gUI": sdl2.KMOD_RGUI,
    "numlock": sdl2.KMOD_NUM,
    "caps lock": sdl2.KMOD_CAPS,
    "altgr": sdl2.KMOD_MODE,
}


def get_name(code: int) -> str:
    """
    Gets the name of a key from its keycode.

    Args:
        code: A keycode.

    Returns:
        str: The corresponding key.
    """
    return sdl2.keyboard.SDL_GetKeyName(code).decode("utf-8").lower()


def key_from_name(char: str) -> int:
    """
    Gets the keycode of a key from its name.

    Args:
        char: The name of the key.

    Returns:
        int: The corresponding keycode.
    """
    return sdl2.keyboard.SDL_GetKeyFromName(c_char_p(bytes(char, "utf-8")))


def scancode_from_name(char: str) -> int:
    """
    Gets the scancode of a key from its name.

    Args:
        char: The name of the key.

    Returns:
        int: The corresponding scancode.
    """
    return sdl2.keyboard.SDL_GetScancodeFromName(c_char_p(bytes(char, "utf-8")))


def window_focused() -> bool:
    """
    Checks if the display has keyboard focus.

    Returns:
        bool: True if the window is focused, false otherwise.
    """
    return sdl2.keyboard.SDL_GetKeyboardFocus() == Display.window or sdl2.mouse.SDL_GetMouseFocus() == Display.window


def get_keyboard_state():
    """ Returns a list with the current SDL keyboard state,
    which is updated on SDL_PumpEvents. """
    numkeys = ctypes.c_int()
    keystate = sdl2.SDL_GetKeyboardState(ctypes.byref(numkeys))
    ptr_t = ctypes.POINTER(ctypes.c_uint8 * numkeys.value)
    return ctypes.cast(keystate, ptr_t)[0]


def key_pressed(*keys: str) -> bool:
    """
    Checks if keys are pressed.

    Args:
        *keys: The names of the keys to check.

    Returns:
        bool: Whether or not the keys are pressed.

    Example:
        .. code-block:: python

            if rb.Input.key_pressed("a"):
                # handle the "a" keypress

            if rb.Input.key_pressed("shift", "w"):
                # handle the "shift+w" keypress

    """
    for key in keys:
        key = key.lower()
        if key in _mods:
            if not sdl2.SDL_GetModState() & _mods[key]:
                return False
        else:
            if not get_keyboard_state()[scancode_from_name(key)]:
                return False
    return True


# MOUSE FUNCTIONS


def mouse_is_pressed() -> Tuple[bool]:
    """
    Checks which mouse buttons are pressed.

    Returns:
        Tuple[bool]: A tuple with 5 booleans representing the state of each
        mouse button. (button1, button2, button3, button4, button5)
    """
    x = c_long(0)
    y = c_long(0)
    info = sdl2.mouse.SDL_GetMouseState(x, y)
    return (
        (info & sdl2.mouse.SDL_BUTTON_LMASK) != 0,
        (info & sdl2.mouse.SDL_BUTTON_MMASK) != 0,
        (info & sdl2.mouse.SDL_BUTTON_RMASK) != 0,
        (info & sdl2.mouse.SDL_BUTTON_X1MASK) != 0,
        (info & sdl2.mouse.SDL_BUTTON_X2MASK) != 0,
    )


def mouse_pos() -> Vector:
    """
    Returns the current position of the mouse.

    Returns:
        Vector: A Vector representing position.
    """
    x = c_long(0)
    y = c_long(0)
    sdl2.mouse.SDL_GetMouseState(x, y)
    return Vector(x, y)


def set_mouse_pos(x: int, y: int):
    """
    Sets the mouse position in the game window.

    Args:
        x: The new x position of the cursor.
        y: The new y position of the cursor.
    """
    sdl2.mouse.SDL_WarpMouseInWindow(Display.window, c_int(x), c_int(y))


def mouse_is_visible() -> bool:
    """
    Checks if the mouse is currently visible.

    Returns:
        bool: True for visible, false otherwise.
    """
    state = sdl2.mouse.SDL_ShowCursor(sdl2.SDL_QUERY)
    return state == sdl2.SDL_ENABLE


def set_mouse_visibility(toggle: bool):
    """
    Sets the mouse visibility.

    Args:
        toggle: True to show the mouse and false to hide the mouse.
    """
    if toggle:
        sdl2.mouse.SDL_ShowCursor(sdl2.SDL_ENABLE)
    else:
        sdl2.mouse.SDL_ShowCursor(sdl2.SDL_DISABLE)


def mouse_over(center: Vector, dims: Vector = Vector(1, 1)) -> bool:
    """
    Checks if the mouse is inside a rectangle defined by its center
    and dimensions

    Args:
        center: The center of the rectangle.
        dims: The dimensions of the rectangle. Defaults to Vector(1, 1).

    Returns:
        bool: Whether or not the mouse is in the defined rectangle.
    """
    top_left = (center - dims / 2).ceil()
    bottom_right = (center + dims / 2).ceil()

    return top_left.x <= mouse_pos().x <= bottom_right.x and top_left.y <= mouse_pos().y <= bottom_right.y
