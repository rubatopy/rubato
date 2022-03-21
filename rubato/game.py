"""
The main game class. It controls everything in the game.

Attributes:
    scenes (SceneManager): The global scene manager.
    radio (Radio): The global radio system.
    name (str): The title of the game window.
    fps (int): The target fps of the game.
    reset_display (bool): Controls whether or not the display should reset
        every frame.
    state (STATE): The current state of the game.
"""
from __future__ import unicode_literals
import sys
from typing import TYPE_CHECKING
import sdl2
import sdl2.ext
from rubato.classes.sprite import Sprite
from rubato.utils import Display, Vector, Time, Defaults, Color
from rubato.classes import SceneManager
import rubato.input as Input
from enum import Enum
from contextlib import suppress

if TYPE_CHECKING:
    from rubato.radio import Radio


class STATE(Enum):
    """
    An enum to keep track of the state things

    RUNNING: will run everything normally
    STOPPED: will quit the window
    PAUSED: will pause physics time calls. Please do not use this feature.
    """
    RUNNING = 1
    STOPPED = 2
    PAUSED = 3


sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)

name: str = ""
background_color: Color = Color(0, 0, 0)
foreground_color: Color = Color(255, 255, 255)

_state = STATE.STOPPED
scenes = SceneManager()
radio: "Radio" = None

initialized = False


def init(options: dict = {}):
    """
    Initializes a game. Should only be called by :meth:`rubato.init`.

    Args:
        options: A game config.
            Defaults to the |default| for `Game`.
    """
    global initialized, background_color, foreground_color

    initialized = True

    params = Defaults.game_defaults | options

    background_color = Color(*params["background_color"]) if not isinstance(
        params["background_color"], Color) else params["background_color"]

    foreground_color = Color(*params["foreground_color"]) if not isinstance(
        params["foreground_color"], Color) else params["foreground_color"]

    Time.target_fps = params["target_fps"]
    Time.physics_fps = params["physics_fps"]

    flags = (sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI
             | sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_MOUSE_FOCUS
             | sdl2.SDL_WINDOW_INPUT_FOCUS)

    Display.window = sdl2.ext.Window(params["name"],
                                     params["window_size"].to_tuple(),
                                     flags=flags)

    Display.renderer = sdl2.ext.Renderer(
        Display.window,
        flags=(sdl2.SDL_RENDERER_ACCELERATED
               | sdl2.SDL_RENDERER_PRESENTVSYNC),
        logical_size=params["resolution"].to_tuple())

    if params["icon"] != "":
        Display.set_window_icon(params["icon"])


def constant_loop():
    """
    The constant game loop. Should only be called by :meth:`rubato.begin`.
    """
    global _state
    _state = STATE.RUNNING
    while True:
        update()


def update():
    """
    The update loop for the game. Called automatically every frame.
    Handles the game states.
    Will always process timed calls.
    """

    # Event handling
    for event in sdl2.ext.get_events():
        sdl2.SDL_PumpEvents()
        if event.type == sdl2.SDL_QUIT:
            radio.broadcast("exit")
            sdl2.SDL_Quit()
            sys.exit(1)
        if event.type == sdl2.SDL_WINDOWEVENT:
            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                radio.broadcast(
                    "resize", {
                        "width": event.window.data1,
                        "height": event.window.data2,
                        "old_width": window_size.x,
                        "old_height": window_size.y
                    })
                window_size = Vector(event.window.data1, event.window.data2)
        if event.type in (sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP):
            key_info, unicode = event.key.keysym, ""
            with suppress(ValueError):
                unicode = chr(key_info.sym)

            if event.type == sdl2.SDL_KEYUP:
                event_name = "keyup"
            else:
                event_name = ("keyhold", "keydown")[not event.key.repeat]

            radio.broadcast(
                event_name,
                {
                    "key": Input.get_name(key_info.sym),
                    "unicode": unicode,
                    "code": int(key_info.sym),
                    "modifiers": key_info.mod,
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

    if get_state() == STATE.PAUSED:
        # process user set pause update
        scenes.paused_update()
    else:
        # fixed update
        Time.physics_counter += Time.delta_time
        Time.fixed_delta = 1000 / Time.physics_fps

        while Time.physics_counter >= Time.fixed_delta:
            scenes.fixed_update()
            Time.physics_counter -= Time.fixed_delta

        # normal update
        scenes.update()

    # Draw Loop
    Display.renderer.clear(background_color.to_tuple())
    Display.renderer.fill(
        (
            0,
            0,
            Display.renderer.logical_size[0],
            Display.renderer.logical_size[1],
        ),
        foreground_color.to_tuple(),
    )
    scenes.draw()

    # update renderers
    Display.renderer.present()

    frame_end = sdl2.SDL_GetTicks64()
    Time.delta_time = frame_end - frame_start

    if Time.target_fps > 0:
        delay = (1000 / Time.target_fps) - Time.delta_time
        if delay > 0:
            sdl2.SDL_Delay(int(delay))


def render(sprite: Sprite, surface: sdl2.surface.SDL_Surface):
    if sprite.z_index <= scenes.current.camera.z_index:
        width, height = surface.w, surface.h

        new_size = (
            round(width * scenes.current.camera.zoom),
            round(height * scenes.current.camera.zoom),
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
            scenes.current.camera.transform(sprite.pos - \
                Vector(width, height)/2),
        )


def get_state() -> STATE:
    return _state


def set_state(new_state: STATE):
    global _state
    _state = new_state

    if _state == STATE.STOPPED:
        sdl2.events.SDL_PushEvent(sdl2.events.SDL_QuitEvent())
