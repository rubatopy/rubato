"""
These events are broadcast by rubato and can be listened to with
:func:`rb.Radio.listen() <rubato.utils.radio.Radio.listen>`. Here is an example of how you can listen for a
key down event:

.. code-block:: python

    def listener(data: rb.KeyResponse):
        if data.key == "a":
            print("You pressed the 'a' key!")

    rb.Radio.listen(rb.Events.KEYDOWN, listener)
"""

from __future__ import annotations
from enum import Enum, unique
from dataclasses import dataclass
import cython


@unique
class Events(Enum):
    """
    Describes all rubato-fired events that can be listened for.
    """

    KEYUP = "KEYUP"
    """
    Fired when a key is released.
    Responds with a :func:`KeyResponse <rubato.utils.events.KeyResponse>` object.
    """
    KEYDOWN = "KEYDOWN"
    """
    Fired when a key is pressed.
    Responds with a :func:`KeyResponse <rubato.utils.events.KeyResponse>` object.
    """
    KEYHOLD = "KEYHOLD"
    """
    Fired when a key is held down (After the initial keydown).
    Responds with a :func:`KeyResponse <rubato.utils.events.KeyResponse>` object.
    """
    MOUSEUP = "MOUSEUP"
    """
    Fired when a mouse button is released.
    Responds with a :func:`MouseButtonResponse <rubato.utils.events.MouseButtonResponse>` object.
    """
    MOUSEDOWN = "MOUSEDOWN"
    """
    Fired when a mouse button is pressed.
    Responds with a :func:`MouseButtonResponse <rubato.utils.events.MouseButtonResponse>` object.
    """
    MOUSEWHEEL = "MOUSEWHEEL"
    """
    Fired when the mouse wheel is scrolled.
    Responds with a :func:`MouseWheelResponse <rubato.utils.events.MouseWheelResponse>` object.
    """
    MOUSEMOTION = "MOUSEMOTION"
    """
    Fired when the mouse is moved.
    Responds with a :func:`MouseMotionResponse <rubato.utils.events.MouseMotionResponse>` object.
    """
    JOYAXISMOTION = "JOYAXISMOTION"
    """
    Fired when a controller joystick axis is moved.
    Responds with a :func:`JoyAxisMotionResponse <rubato.utils.events.JoyAxisMotionResponse>` object.
    """
    JOYHATMOTION = "JOYHATMOTION"
    """
    Fired when a controller hat button is changed.
    Responds with a :func:`JoyHatMotionResponse <rubato.utils.events.JoyHatMotionResponse>` object.
    """
    JOYBUTTONDOWN = "JOYBUTTONDOWN"
    """
    Fired when a controller button is pressed.
    Responds with a :func:`JoyButtonResponse <rubato.utils.events.JoyButtonResponse>` object.
    """
    JOYBUTTONUP = "JOYBUTTONUP"
    """
    Fired when a controller button is released.
    Responds with a :func:`JoyButtonResponse <rubato.utils.events.JoyButtonResponse>` object.
    """
    EXIT = "EXIT"
    """Fired when the game is exiting. Has no response."""
    RESIZE = "RESIZE"
    """
    Fired when the window is resized.
    Responds with a :func:`ResizeResponse <rubato.utils.events.ResizeResponse>` object.
    """


if not cython.compiled:
    from enum_tools import document_enum
    document_enum(Events)


@dataclass(frozen=True)
class EventResponse:
    """A response to an event. This class behaves like a dict, but is immutable."""
    timestamp: int
    """The timestamp of the event in seconds."""

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            raise KeyError(item)

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def values(self):
        return self.__dict__.values()

    def get(self, item, default=None):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            return default


@dataclass(frozen=True)
class KeyResponse(EventResponse):
    """A response to a key event"""
    key: str
    """The name of the key (see Key Names section for the list of possible key names)"""
    unicode: str
    """The unicode character for the key (keys without unicode are just empty strings)"""
    code: int
    """The keycode of the the key. (can be processed with Input.get_name)"""
    mods: int
    """The code for the currently pressed modifiers. (can be processed with Input.mods_from_code)"""


@dataclass(frozen=True)
class MouseButtonResponse(EventResponse):
    """A response to a mouse event"""
    button: int
    """The mouse button that was pressed"""
    x: int
    """The x position of the mouse"""
    y: int
    """The y position of the mouse"""
    clicks: int
    """The number of clicks that have been made"""
    which: int
    """The mouse that was used"""


@dataclass(frozen=True)
class MouseWheelResponse(EventResponse):
    """A response to a mouse wheel event"""
    x: float
    """The x scroll amount of the mouse"""
    y: float
    """The y scroll amount of the mouse"""
    which: int
    """The mouse that was used"""


@dataclass(frozen=True)
class MouseMotionResponse(EventResponse):
    """A response to a mouse motion event"""
    x: int
    """The x position of the mouse"""
    y: int
    """The y position of the mouse"""
    dx: int
    """The change in x position of the mouse"""
    dy: int
    """The change in y position of the mouse"""
    which: int
    """The mouse that was used"""


@dataclass(frozen=True)
class JoyAxisMotionResponse(EventResponse):
    """A response to a joystick axis event"""
    controller: int
    """The joystick that was used"""
    axis: int
    """The axis that was moved"""
    value: float
    """The value of the axis"""
    centered: bool
    """Whether the axis is centered"""


@dataclass(frozen=True)
class JoyButtonResponse(EventResponse):
    """A response to a joystick button event"""
    controller: int
    """The joystick that was used"""
    button: int
    """The button that was pressed"""


@dataclass(frozen=True)
class JoyHatMotionResponse(EventResponse):
    """A response to a joystick hat event"""
    controller: int
    """The joystick that was used"""
    hat: int
    """The hat that was moved"""
    value: int
    """The value of the hat"""
    name: str
    """The name of the hat"""


@dataclass(frozen=True)
class ResizeResponse(EventResponse):
    """A response to a resize event"""
    width: int
    """The new width of the window"""
    height: int
    """The new height of the window"""
    old_width: float
    """The old width of the window"""
    old_height: float
    """The old height of the window"""
