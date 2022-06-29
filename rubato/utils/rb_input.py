"""
The Input module is the way you collect input from the user.
"""
import ctypes
from typing import Tuple, List, Dict
import sdl2
from ctypes import c_char_p, c_float, c_int

from . import Vector, Display


class Input:
    """
    The input class, handling keyboard and mouse getter and setter functionality

    Go :doc:`here <key-names>` for a list of all the available keys.
    """
    # KEYBOARD METHODS

    _mods: Dict[str, int] = {
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
        "right gui": sdl2.KMOD_RGUI,
        "numlock": sdl2.KMOD_NUM,
        "caps lock": sdl2.KMOD_CAPS,
        "altgr": sdl2.KMOD_MODE,
    }

    @classmethod
    def key_pressed(cls, *keys: str) -> bool:
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
            if key in cls._mods and len(keys) > 1:
                if not sdl2.SDL_GetModState() & cls._mods[key]:
                    return False
            else:
                if key == "shift":
                    key1, key2 = "left shift", "right shift"
                elif key == "ctrl":
                    key1, key2 = "left ctrl", "right ctrl"
                elif key == "alt":
                    key1, key2 = "left alt", "right alt"
                elif key == "gui":
                    key1, key2 = "left gui", "right gui"
                else:
                    key1, key2 = key, key

                if not (
                    cls.get_keyboard_state()[cls.scancode_from_name(key1)] or
                    cls.get_keyboard_state()[cls.scancode_from_name(key2)]
                ):
                    return False
        return True

    @classmethod
    def get_keyboard_state(cls):
        """Returns a list with the current SDL keyboard state."""
        numkeys = ctypes.c_int()
        keystate = sdl2.SDL_GetKeyboardState(ctypes.byref(numkeys))
        ptr_t = ctypes.POINTER(ctypes.c_uint8 * numkeys.value)
        return ctypes.cast(keystate, ptr_t)[0]

    @classmethod
    def get_name(cls, code: int) -> str:
        """
        Gets the name of a key from its keycode.

        Args:
            code: A keycode.

        Returns:
            str: The corresponding key.
        """
        return sdl2.SDL_GetKeyName(code).decode("utf-8").lower()

    @classmethod
    def mods_from_code(cls, code: int) -> List[str]:
        """
        Gets the modifier names from a mod code.

        Args:
            code: The mod code.

        Returns:
            List[str]: A list with the names of the currently pressed modifiers.
        """
        return [name for name, val in cls._mods.items() if code & val]

    @classmethod
    def key_from_name(cls, char: str) -> int:
        """
        Gets the keycode of a key from its name.

        Args:
            char: The name of the key.

        Returns:
            int: The corresponding keycode.
        """
        return sdl2.SDL_GetKeyFromName(c_char_p(bytes(char, "utf-8")))

    @classmethod
    def scancode_from_name(cls, char: str) -> int:
        """
        Gets the scancode of a key from its name.

        Args:
            char: The name of the key.

        Returns:
            int: The corresponding scancode.
        """
        return sdl2.SDL_GetScancodeFromName(c_char_p(bytes(char, "utf-8")))

    @classmethod
    def window_focused(cls) -> bool:
        """
        Checks if the display has keyboard focus.

        Returns:
            bool: True if the window is focused, false otherwise.
        """
        return sdl2.SDL_GetKeyboardFocus() == Display.window or sdl2.SDL_GetMouseFocus(
        ) == Display.window

    # MOUSE FUNCTIONS

    @classmethod
    def mouse_state(cls) -> Tuple[bool]:
        """
        Checks which mouse buttons are pressed.

        Returns:
            Tuple[bool]: A tuple with 5 booleans representing the state of each
            mouse button. (button1, button2, button3, button4, button5)
        """
        info = sdl2.SDL_GetMouseState(ctypes.pointer(c_int(0)), ctypes.pointer(c_int(0)))
        return (
            (info & sdl2.SDL_BUTTON_LMASK) != 0,
            (info & sdl2.SDL_BUTTON_MMASK) != 0,
            (info & sdl2.SDL_BUTTON_RMASK) != 0,
            (info & sdl2.SDL_BUTTON_X1MASK) != 0,
            (info & sdl2.SDL_BUTTON_X2MASK) != 0,
        )

    @classmethod
    def mouse_pressed(cls) -> bool:
        """
        Checks if any mouse button is pressed.

        Returns:
            True if any button is pressed, false otherwise.
        """
        return any(cls.mouse_state())

    @staticmethod
    def get_mouse_pos() -> Vector:
        """
        The current position of the mouse.

        Returns:
            Vector: A Vector representing position.
        """
        x_window, y_window = c_int(0), c_int(0)
        sdl2.SDL_GetMouseState(ctypes.pointer(x_window), ctypes.pointer(y_window))

        x_render, y_render = c_float(0), c_float(0)
        sdl2.SDL_RenderWindowToLogical(Display.renderer.sdlrenderer, x_window, y_window, x_render, y_render)

        # size = Display.border_size
        # if Display.has_x_border:
        #     x_window.value = min(max(x_window.value, size), Display.window_size.x + size) - size
        # elif Display.has_y_border:
        #     y_window.value = min(max(y_window.value, size), Display.window_size.y + size) - size
        return Vector(x_render.value, y_render.value).clamp(Vector(0, 0), Display.window_size)

    @staticmethod
    def get_mouse_abs_pos() -> Vector:
        """
        The current absolute position of the mouse. ie. screen coordinates.
        Returns:
            A Vector representing position.
        """
        x_window, y_window = c_int(0), c_int(0)
        sdl2.SDL_GetMouseState(ctypes.pointer(x_window), ctypes.pointer(y_window))
        return Vector(x_window.value, y_window.value)

    @staticmethod
    def set_mouse_pos(v: Vector):
        sdl2.SDL_WarpMouseInWindow(Display.window.window, c_int(v.x), c_int(v.y))

    @classmethod
    def mouse_is_visible(cls) -> bool:
        """
        Checks if the mouse is currently visible.

        Returns:
            bool: True for visible, false otherwise.
        """
        return sdl2.SDL_ShowCursor(sdl2.SDL_QUERY) == sdl2.SDL_ENABLE

    @classmethod
    def set_mouse_visibility(cls, toggle: bool):
        """
        Sets the mouse visibility.

        Args:

            toggle: True to show the mouse and false to hide the mouse.
        """
        sdl2.SDL_ShowCursor(sdl2.SDL_ENABLE if toggle else sdl2.SDL_DISABLE)

    @classmethod
    def mouse_in(cls, center: Vector, dims: Vector = Vector(1, 1), angle: float = 0) -> bool:
        """
        Checks if the mouse is inside a rectangle defined by its center
        and dimensions

        Args:
            center: The center of the rectangle.
            dims: The dimensions of the rectangle. Defaults to Vector(1, 1).
            angle: The angle of the rectangle in degrees. Defaults to 0.

        Returns:
            bool: Whether or not the mouse is in the defined rectangle.
        """

        mo = Input.get_mouse_pos()  # mouse

        if angle == 0:
            lt = (center - dims / 2).ceil()  # left top
            rb = (center + dims / 2).ceil()  # right bottom
            return lt.x <= mo.x <= rb.x and lt.y <= mo.y <= rb.y
        else:
            lt = (-dims / 2).rotate(angle) + center  # left top
            rt = (Vector(dims.x, -dims.y) / 2).rotate(angle) + center  # right top
            rb = (dims / 2).rotate(angle) + center  # right bottom
            lb = (Vector(-dims.x, dims.y) / 2).rotate(angle) + center  # left bottom

            return (
                cls._is_left(lt, rt, mo) and cls._is_left(rt, rb, mo) and cls._is_left(rb, lb, mo) and
                cls._is_left(lb, lt, mo)
            )

    @staticmethod
    def _is_left(p0: Vector, p1: Vector, p2: Vector) -> bool:
        # not sure what this does but I got it from:
        # https://gamedev.stackexchange.com/a/110233
        return ((p1.x - p0.x) * (p2.y - p0.y) - (p2.x - p0.x) * (p1.y - p0.y)) > 0
