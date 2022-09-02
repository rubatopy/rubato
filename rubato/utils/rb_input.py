"""
An abstraction for checking for hardware input from a user.
"""
import ctypes
import math
import sdl2
from ctypes import c_char_p, c_float, c_int

from . import Vector, Display, Math, InitError


# THIS IS A STATIC CLASS
class Input:
    """
    The input class, handling keyboard, mouse, and controller functionality.

    Go :doc:`here <key-names>` for a list of all the available keys.
    """
    # CONTROLLER METHODS

    _controllers: list[sdl2.SDL_Joystick] = []
    _joystick_max: int = 32768

    @classmethod
    @property
    def controllers(cls) -> int:
        """
        The number of controllers currently registered. (get-only)

        If non-zero, the controllers are registered from 0 to n-1 where n is the number of controllers.
        This number index is passed to events that are propagated when controllers are inputted to.

        Returns:
            int: The total number of controllers.
        """
        return len(cls._controllers)

    @classmethod
    def update_controllers(cls) -> None:
        """
        Register or deregister controllers as needed. Called automatically.
        """
        conts = sdl2.SDL_NumJoysticks()
        length = len(cls._controllers)

        if conts == length:
            return

        elif conts > length:
            if length == 0:
                sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)
            for i in range(length, conts):
                cls._controllers.append(sdl2.SDL_JoystickOpen(i))
            return

        for i in range(length):
            sdl2.SDL_JoystickClose(cls._controllers[i])
        cls._controllers = []
        if conts > 0:
            for i in range(conts):
                cls._controllers.append(sdl2.SDL_JoystickOpen(i))
        else:
            sdl2.SDL_JoystickEventState(sdl2.SDL_DISABLE)

    @classmethod
    def controller_name(cls, controller: int) -> str:
        """
        Get the name of the controller at the given index.

        Args:
            index (int): The index of the controller to get the name of.

        Raises:
            IndexError: If the index is out of range.
                Note that no error is thrown if controller is negative.

        Returns:
            str: The name of the controller. If controller is less than 0, returns an empty string.
        """
        if controller < 0:
            return ""
        if controller >= len(cls._controllers):
            raise IndexError(f"Index {controller} out of range.")
        return sdl2.SDL_JoystickNameForIndex(controller)

    @classmethod
    def controller_axis(cls, controller: int, axis: int) -> float:
        """
        Get the value of a given joystick axis on a controller.

        Args:
            controller: The index of the controller.
            axis: The index of the joystick axis.

        Raises:
            IndexError: The given controller index is out of range.
                Note that no error is thrown if controller is negative.

        Returns:
            The value of the axis. If controller is less than 0, returns 0.
        """
        if controller < 0:
            return 0
        if controller >= len(cls._controllers):
            raise IndexError(f"Index {controller} out of range.")
        return sdl2.SDL_JoystickGetAxis(cls._controllers[controller], axis) / cls._joystick_max

    @classmethod
    def axis_centered(cls, val: float) -> bool:
        """
        Check whether a given axis value is within the +/-10% bounds of deadzone considered the "center".

        Args:
            val: The value of the axis.

        Returns:
            Whether the axis is centered.
        """
        return -0.1 < val < 0.1

    @classmethod
    def controller_button(cls, controller: int, button: int) -> bool:
        """
        Get whether a given button on a controller is pressed.

        Args:
            controller (int): The index of the controller.
            button (int): The index of the button.

        Raises:
            IndexError: The given controller index is out of range.
                Note that no error is thrown if controller is negative.

        Returns:
            bool: Whether the button is pressed. If controller is less than 0, returns False.
        """
        if controller < 0:
            return False
        if controller >= len(cls._controllers):
            raise IndexError(f"Index {controller} out of range.")
        return sdl2.SDL_JoystickGetButton(cls._controllers[controller], button) == 1

    @classmethod
    def controller_hat(cls, controller: int, hat: int) -> int:
        """
        Get the value of a given hat on a controller.

        Args:
            controller (int): The index of the controller.
            hat (int): The index of the hat.

        Raises:
            IndexError: The given controller index is out of range.
                Note that no error is thrown if controller is negative.

        Returns:
            int: The value of the hat, which you can translate with `translate_hat()`.
                If controller is less than 0, returns 0.
        """
        if controller < 0:
            return 0
        if controller >= len(cls._controllers):
            raise IndexError(f"Index {controller} out of range.")
        return sdl2.SDL_JoystickGetHat(cls._controllers[controller], hat)

    @classmethod
    def translate_hat(cls, val: int) -> str:
        """
        Translate a hat value to a string.

        Args:
            val (int): The hat value.

        Returns:
            str: The string representation of the hat value.
        """
        if val & sdl2.SDL_HAT_CENTERED:
            return "center"
        elif val & sdl2.SDL_HAT_UP:
            return "up"
        elif val & sdl2.SDL_HAT_RIGHT:
            return "right"
        elif val & sdl2.SDL_HAT_DOWN:
            return "down"
        elif val & sdl2.SDL_HAT_LEFT:
            return "left"
        elif val & sdl2.SDL_HAT_RIGHTUP:
            return "right up"
        elif val & sdl2.SDL_HAT_RIGHTDOWN:
            return "right down"
        elif val & sdl2.SDL_HAT_LEFTUP:
            return "left up"
        elif val & sdl2.SDL_HAT_LEFTDOWN:
            return "left down"
        return "unknown"

    # KEYBOARD METHODS

    _mods: dict[str, int] = {
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

    def __init__(self) -> None:
        raise InitError(self)

    @classmethod
    def key_pressed(cls, *keys: str) -> bool:
        """
        Checks if keys are pressed. Case insensitive.

        Args:
            *keys: The names of the keys to check.

        Returns:
            bool: Whether the keys are pressed.

        Example:
            .. code-block:: python

                if rb.Input.key_pressed("a"):
                    # handle the "a" keypress

                if rb.Input.key_pressed("shift", "w"):
                    # handle the "shift+w" keypress
        """
        state = cls.get_keyboard_state()

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

                if not (state[cls.scancode_from_name(key1)] or state[cls.scancode_from_name(key2)]):
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
    def mods_from_code(cls, code: int) -> list[str]:
        """
        Gets the modifier names from a mod code.

        Args:
            code: The mod code.

        Returns:
            list[str]: A list with the names of the currently pressed modifiers.
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
        return sdl2.SDL_GetKeyboardFocus() == Display.window or sdl2.SDL_GetMouseFocus() == Display.window

    # MOUSE FUNCTIONS

    @classmethod
    def mouse_state(cls) -> tuple[bool, bool, bool, bool, bool]:
        """
        Checks which mouse buttons are pressed.

        Returns:
            A tuple with 5 booleans representing the state of each
            mouse button. (button1, button2, button3, button4, button5)
        """
        info = sdl2.SDL_GetMouseState(ctypes.byref(c_int(0)), ctypes.byref(c_int(0)))
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
        The current position of the mouse, in screen-coordinates.

        Returns:
            A Vector representing position.
        """
        x_window, y_window = c_int(0), c_int(0)
        sdl2.SDL_GetMouseState(ctypes.byref(x_window), ctypes.byref(y_window))

        x_render, y_render = c_float(0), c_float(0)
        size = Display.border_size
        if Display.has_x_border():
            x_window.value = math.floor(Math.clamp(x_window.value, size, Display.window_size.x - size))
        elif Display.has_y_border():
            y_window.value = math.floor(Math.clamp(y_window.value, size, Display.window_size.y - size))
        sdl2.SDL_RenderWindowToLogical(Display.renderer.sdlrenderer, x_window, y_window, x_render, y_render)

        return Vector(x_render.value, y_render.value)

    @staticmethod
    def get_mouse_abs_pos() -> Vector:
        """
        The current absolute position of the mouse. ie. screen coordinates.

        Returns:
            A Vector representing position.
        """
        x_window, y_window = c_int(0), c_int(0)
        sdl2.SDL_GetMouseState(ctypes.byref(x_window), ctypes.byref(y_window))
        return Vector(x_window.value, y_window.value)

    @staticmethod
    def set_mouse_pos(v: Vector | tuple[float, float]):
        """
        Sets the position of the mouse.

        Args:
            v: The position to set the mouse to.
        """
        sdl2.SDL_WarpMouseInWindow(Display.window.window, c_int(round(v[0])), c_int(round(v[1])))

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

    @staticmethod
    def pt_in_poly(pt: Vector | tuple[float, float], verts: list[Vector] | list[tuple[float, float]]) -> bool:
        """
        Checks if a point is inside a polygon.

        Args:
            pt: The point to check.
            verts: The polygon representation as a list of Vector | tuple[float, float]s (vertices)

        Returns:
            bool: Whether the point is inside the polygon.
        """
        last, now, odd = verts[-1], verts[0], False
        for now in verts:
            if ((now[1] > pt[1]) != (last[1] > pt[1])) and \
                (pt[0] < (last[0] - now[0]) * (pt[1] - now[1]) / (last[1] - now[1]) + now[0]):
                odd = not odd
            last = now

        return odd

    @classmethod
    def mouse_in(
        cls,
        center: Vector | tuple[float, float],
        dims: Vector | tuple[float, float] = (1, 1),
        angle: float = 0
    ) -> bool:
        """
        Checks if the mouse is inside a rectangle defined by its center
        and dimensions

        Args:
            center: The center of the rectangle.
            dims: The dimensions of the rectangle. Defaults to (1, 1).
            angle: The angle of the rectangle in degrees. Defaults to 0.

        Returns:
            bool: Whether the mouse is in the defined rectangle.
        """
        center = Vector.create(center)
        dims = Vector.create(dims)

        mo = Input.get_mouse_pos()  # mouse

        if angle == 0:
            lt = (center - dims / 2).ceil()  # left top
            rb = (center + dims / 2).ceil()  # right bottom
            return lt.x <= mo.x <= rb.x and lt.y <= mo.y <= rb.y
        else:
            lt = (-dims / 2).rotate(angle) + center  # left top # pylint: disable=invalid-unary-operand-type
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
