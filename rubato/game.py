"""
The main game module. It controls everything in the game.
"""
from __future__ import annotations
import sys
import sdl2, sdl2.ext, sdl2.sdlttf
from contextlib import suppress
from typing import TYPE_CHECKING

from . import Time, Display, Vector, Color, Input, Radio, Font, Draw

if TYPE_CHECKING:
    from . import SceneManager, Camera


class GameProperties(type):
    """
    Defines static property methods for Game.

    Warning:
        This is only a metaclass for the class below it, so you wont be able to access this class.
        To use the property methods here, simply access them as you would any other Game property.
    """

    @property
    def state(cls) -> int:
        """
        The state of the game.

        The game states are::

            Game.RUNNING
            Game.STOPPED
            Game.PAUSED
        """
        return cls._state

    @state.setter
    def state(cls, new: int):
        cls._state = new

        if cls._state == Game.STOPPED:
            sdl2.events.SDL_PushEvent(sdl2.SDL_Event(sdl2.events.SDL_QUIT))

    @property
    def camera(cls) -> Camera:
        """
        A shortcut getter allowing easy access to the current camera.
        This is a get-only property.

        Note:
            Returns a pointer to the current camera object.
            This is so you can access/change the current camera properties faster, but you'd still need to
            use :func:`Game.scenes.current.camera <rubato.classes.scene.Scene.camera>` to access the camera directly.

        Returns:
            Camera: The current scene's camera
        """
        return cls.scenes.current.camera


class Game(metaclass=GameProperties):
    """
    The main game class.

    Attributes:
        name (str): The title of the game window.
        scenes (SceneManager): The global scene manager.
        background_color (Color): The background color of the window.
        border_color (Color): The color of the borders of the window.
        debug (bool): Turn on debug rendering for everything in the game.
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3

    name: str = ""
    border_color: Color = Color(0, 0, 0)
    background_color: Color = Color(255, 255, 255)

    debug: bool = False
    show_fps: bool = False
    debug_font: Font

    _state: int = STOPPED
    scenes: SceneManager = None

    initialized = False

    @classmethod
    def constant_loop(cls):
        """
        The constant game loop. Should only be called by :meth:`rubato.begin`.
        """
        cls.state = cls.RUNNING
        while True:
            cls.update()

    @classmethod
    def update(cls):
        """
        The update loop for the game. Called automatically every frame.
        Handles the game states.
        Will always process timed calls.
        """
        # start timing the update loop
        frame_start = sdl2.SDL_GetTicks64()

        # Event handling
        for event in sdl2.ext.get_events():
            sdl2.SDL_PumpEvents()
            if event.type == sdl2.SDL_QUIT:
                Radio.broadcast("EXIT")
                sdl2.sdlttf.TTF_Quit()
                sdl2.SDL_Quit()
                sys.exit()
            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    Radio.broadcast(
                        "RESIZE", {
                            "width": event.window.data1,
                            "height": event.window.data2,
                            "old_width": Display.window_size.x,
                            "old_height": Display.window_size.y
                        }
                    )
                    Display.window_size = Vector(
                        event.window.data1,
                        event.window.data2,
                    )
            if event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
                key_info, unicode = event.key.keysym, ""
                with suppress(ValueError):
                    unicode = chr(key_info.sym)

                if event.type == sdl2.SDL_KEYUP:
                    event_name = "KEYUP"
                else:
                    event_name = ("KEYDOWN", "KEYHOLD")[event.key.repeat]

                Radio.broadcast(
                    event_name,
                    {
                        "key": Input.get_name(key_info.sym),
                        "unicode": unicode,
                        "code": int(key_info.sym),
                        "mods": key_info.mod,
                    },
                )

        # process delayed calls
        Time.process_calls()

        if cls.state == Game.PAUSED:
            # process user set pause update
            cls.scenes.paused_update()
        else:
            # fixed update
            Time.physics_counter += Time.delta_time

            while Time.physics_counter >= Time.fixed_delta:
                if cls.state != Game.PAUSED:
                    cls.scenes.fixed_update()
                Time.physics_counter -= Time.fixed_delta
            # normal update
            cls.scenes.update()

        # Draw Loop
        Display.renderer.clear(cls.border_color.to_tuple())
        Display.renderer.fill(
            (0, 0, *Display.renderer.logical_size),
            cls.background_color.to_tuple(),
        )
        cls.scenes.draw()

        if cls.show_fps:
            fs = str(int(Time.smooth_fps))
            h = Display.res.y // 40
            p = h // 4
            p2 = p + p
            Draw.rect(
                Vector(p2 + (h * len(fs)) / 2, p2 + h / 2),
                h * len(fs) + p2,
                h + p2,
                Color(a=180),
                fill=Color(a=180),
            )
            Draw.text(fs, font=cls.debug_font, pos=Vector(p2, p2), align=Vector(1, 1))

        # update renderers
        Display.renderer.present()

        # use delay to cap the fps if need be
        if Time.capped:
            delay = Time.normal_delta - Time.delta_time
            if delay > 0:
                sdl2.SDL_Delay(int(delay))

        # dont allow updates to occur more than once in a millisecond
        # this will likely never occur but is a failsafe
        while sdl2.SDL_GetTicks64() == frame_start:
            sdl2.SDL_Delay(1)

        # clock the time the update call took
        Time.delta_time = sdl2.SDL_GetTicks64() - frame_start
