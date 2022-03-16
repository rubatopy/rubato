"""
The main game class. It controls everything in the game.
The Display is where your game lives at a certain aspect ratio,
The Screen is the actual size of the window which the user interacts with.

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
import sdl2
import sdl2.ext
from rubato.classes.sprite import Sprite
from rubato.utils import Display, Vector, Time, Configs
from rubato.classes import SceneManager
from rubato.radio import Radio
import rubato.input as Input
from enum import Enum
from contextlib import suppress


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
window_size: Vector = Vector()
resolution: Vector = Vector()

_state = STATE.STOPPED
scenes = SceneManager()
radio: "Radio" = Radio()

_saved_dims = window_size.clone()

reset_display = False
initialized = False


def init(options: dict = {}):
    """
    Initializes a game. Should only be called by :meth:`rubato.init`.

    Args:
        options: A game config.
            Defaults to the |default| for `Game`.
    """
    global name, window_size, resolution, \
        _saved_dims, initialized, reset_display

    initialized = True

    params = Configs.game_defaults | options

    name = params["name"]
    window_size = params["window_size"]
    resolution = params["resolution"]
    reset_display = params["reset_display"]

    Time.target_fps = params["target_fps"]
    Time.physics_fps = params["physics_fps"]

    flags = (sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI)
    Display.window = sdl2.ext.Window(name, window_size.to_tuple(), flags=flags)

    Display.renderer = sdl2.ext.Renderer(
        Display.window.get_surface(),
        flags=(sdl2.SDL_RENDERER_ACCELERATED
               | sdl2.SDL_RENDERER_PRESENTVSYNC),
        logical_size=resolution.to_tuple())

    Display.set_window_name(name)
    if options.get("icon"):
        Display.set_window_icon(options.get("icon"))

    _saved_dims = window_size.clone()


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
    global _saved_dims

    # Event handling
    for event in sdl2.ext.get_events():
        sdl2.SDL_PumpEvents()
        if event.type == sdl2.SDL_QUIT:
            radio.broadcast("exit")
            sdl2.SDL_Quit()
            sys.exit(1)
        if event.type == sdl2.SDL_WINDOWEVENT_SIZE_CHANGED:
            global window_size
            radio.broadcast(
                "resize", {
                    "width": event.window.data1,
                    "height": event.window.data2,
                    "old_width": window_size.x,
                    "old_height": window_size.y
                })
            window_size = Vector.from_tuple(event.size)
        if event.type == sdl2.SDL_KEYDOWN:
            key_info = event.key.keysym
            unicode = ""
            with suppress(ValueError):
                unicode = chr(key_info.sym)
            radio.broadcast(
                "keyhold" if event.key.repeat > 0 else "keydown",
                {
                    "key": Input.get_name(key_info.sym),
                    "unicode": unicode,
                    "code": int(key_info.sym),
                    "modifiers": key_info.mod,
                },
            )
        if event.type == sdl2.SDL_KEYUP:
            key_info = event.key.keysym
            unicode = ""
            with suppress(ValueError):
                unicode = chr(key_info.sym)
            radio.broadcast(
                "keyup",
                {
                    "key": Input.get_name(key_info.sym),
                    "unicode": unicode,
                    "code": int(key_info.sym),
                    "modifiers": key_info.mod,
                },
            )

    # Window resize handling
    aspect_ratio = resolution.x / resolution.y
    ratio = (window_size.x / window_size.y) < aspect_ratio
    width = (window_size.y * aspect_ratio, window_size.x)[ratio]
    height = (window_size.y, window_size.x / aspect_ratio)[ratio]
    new_top_left = (
        (
            int((window_size.x - width) // 2),
            0,
        ),
        (
            0,
            int((window_size.y - height) // 2),
        ),
    )[ratio]

    sdl2.SDL_RenderSetViewport(
        Display.renderer.sdlrenderer,
        sdl2.SDL_Rect(
            *new_top_left,
            int(width * 2),
            int(height * 2),
        ),
    )

    _saved_dims = window_size.clone()

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
    sdl2.ext.draw.fill(Display.window.get_surface(), (0, 0, 0))
    if reset_display:
        Display.renderer.fill(
            sdl2.SDL_Rect(0, 0, resolution.x, resolution.y),
            sdl2.ext.Color(255, 255, 255, 255),
        )
    scenes.draw()

    # update renderers
    Display.window.refresh()
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


# window dimension getters
def get_width():
    return resolution.x


def get_height():
    return resolution.y


# window position getters
def top_left():
    return Vector(0, 0)


def top_right():
    return Vector(resolution.x, 0)


def bottom_left():
    return Vector(0, resolution.y)


def bottom_right():
    return Vector(resolution.x, resolution.y)


def top_center():
    return Vector(resolution.x / 2, 0)


def bottom_center():
    return Vector(resolution.x / 2, resolution.y)


def center_left():
    return Vector(0, resolution.y / 2)


def center_right():
    return Vector(resolution.x, resolution.y / 2)


def center():
    return Vector(resolution.x / 2, resolution.y / 2)
