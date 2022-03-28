"""
The main game class. It controls everything in the game.
"""
import sys
import sdl2
import sdl2.ext
import sdl2.sdlgfx
from typing import TYPE_CHECKING
from rubato.utils import Time, Display, Vector, Color
from rubato.radio import Radio
import rubato.input as Input
from contextlib import suppress

if TYPE_CHECKING:
    from rubato.classes import SceneManager, Camera


class Game:
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

    _state: int = STOPPED
    scenes: "SceneManager" = None

    initialized = False

    @classmethod
    def __get_state(cls) -> int:
        """
        The state of the game.

        The game states are::

            Game.RUNNING
            Game.STOPPED
            Game.PAUSED
        """
        return cls._state

    @classmethod
    def __set_state(cls, new: int):
        cls._state = new

        if cls._state == Game.STOPPED:
            sdl2.events.SDL_PushEvent(sdl2.events.SDL_QuitEvent())

    state = classmethod(property(__get_state, __set_state, doc=__get_state.__doc__))

    @classmethod
    @property
    def camera(cls) -> "Camera":
        """
        A getter allowing easy access to the current camera.

        Note:
            This is a get-only property but returns a pointer to the current camera object.
            This is so you can access/change the current camera properties faster, but you'd still need to
            use :func:`Game.scenes.current.camera <rubato.classes.scene.Scene.camera>` to access the camera directly.

        Returns:
            Camera: The current scene's camera
        """
        return cls.scenes.current.camera

    @classmethod
    def constant_loop(cls):
        """
        The constant game loop. Should only be called by :meth:`rubato.begin`.
        """
        cls.state = Game.RUNNING
        while True:
            cls.update()

    @classmethod
    def update(cls):
        """
        The update loop for the game. Called automatically every frame.
        Handles the game states.
        Will always process timed calls.
        """

        # Event handling
        for event in sdl2.ext.get_events():
            sdl2.SDL_PumpEvents()
            if event.type == sdl2.SDL_QUIT:
                Radio.broadcast("exit")
                sdl2.SDL_Quit()
                sys.exit(1)
            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    Radio.broadcast(
                        "resize", {
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
                    event_name = "keyup"
                else:
                    event_name = ("keydown", "keyhold")[event.key.repeat]

                Radio.broadcast(
                    event_name,
                    {
                        "key": Input.get_name(key_info.sym),
                        "unicode": unicode,
                        "code": int(key_info.sym),
                        "mods": key_info.mod,
                    },
                )

        if Time.delta_time < 1:
            frame_start = sdl2.SDL_GetTicks64()
            sdl2.SDL_Delay(1)
            frame_end = sdl2.SDL_GetTicks64()
            Time.delta_time = frame_end - frame_start

        frame_start = sdl2.SDL_GetTicks64()

        # process delayed calls
        Time.process_calls()

        if cls.state == Game.PAUSED:
            # process user set pause update
            cls.scenes.paused_update()
        else:
            # fixed update
            Time.physics_counter += Time.delta_time
            Time.fixed_delta = 1000 / Time.physics_fps

            while Time.physics_counter >= Time.fixed_delta:
                cls.scenes.fixed_update()
                Time.physics_counter -= Time.fixed_delta

            # normal update
            cls.scenes.update()

        # Draw Loop
        Display.renderer.clear(cls.border_color.to_tuple())
        Display.renderer.fill(
            (
                0,
                0,
                Display.renderer.logical_size[0],
                Display.renderer.logical_size[1],
            ),
            cls.background_color.to_tuple(),
        )
        cls.scenes.draw()

        if cls.debug:
            # make this actually draw using sdl.ttf font rendering
            sdl2.sdlgfx.stringRGBA(
                Display.renderer.sdlrenderer, 0, 0, f"{int(Time.smooth_fps)}".encode(), 0, 255, 0, 255
            )

        # update renderers
        Display.renderer.present()

        frame_end = sdl2.SDL_GetTicks64()
        Time.delta_time = frame_end - frame_start

        if Time.target_fps > 0:
            delay = (1000 / Time.target_fps) - Time.delta_time
            if delay > 0:
                sdl2.SDL_Delay(int(delay))

    @classmethod
    def render(cls, pos: Vector, z_index: int, surface: sdl2.surface.SDL_Surface):
        """
        Renders a surface to the display.

        Args:
            pos: The position to render the surface at.
            z_index: The z index to use for the surface.
            surface: The surface to render.
        """
        if z_index <= cls.scenes.current.camera.z_index:
            width, height = surface.w, surface.h

            new_size = (
                round(width * cls.scenes.current.camera.zoom),
                round(height * cls.scenes.current.camera.zoom),
            )

            surface_scaled = sdl2.surface.SDL_CreateRGBSurfaceWithFormat(
                0,
                new_size[0],
                new_size[1],
                64,
                sdl2.SDL_PIXELFORMAT_RGBA32,
            )

            sdl2.surface.SDL_BlitScaled(
                surface,
                None,
                surface_scaled,
                sdl2.rect.SDL_Rect(0, 0, new_size[0], new_size[1]),
            )

            Display.update(
                surface_scaled,
                cls.scenes.current.camera.transform(pos - Vector(width, height) / 2),
            )
