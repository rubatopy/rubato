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
import sys
import sdl2
import sdl2.ext
from typing import TYPE_CHECKING, Tuple
from rubato.classes.sprite import Sprite
from rubato.utils import Display, Vector, Time, Configs, Math
from rubato.classes import SceneManager
import rubato.input as Input
from enum import Enum

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
window_size: Vector = Vector()
resolution: Vector = Vector()
fps_cap: int = 0
physics_timestep: int = 0
reset_display: bool = True
_use_better_clock: bool = True

_physics_count: float = 0

_state = STATE.STOPPED

scenes = SceneManager()
radio: "Radio" = None

_saved_dims = window_size.clone()

_clock = None
Time.set_clock(_clock)

_max_screen_size: Tuple[int, int] = (0, 0)

is_init = False


def init(options: dict = {}):
    """
    Initializes a game. Should only be called by :meth:`rubato.init`.

    Args:
        options: A game config.
            Defaults to the |default| for `Game`.
    """
    global name, window_size, resolution, fps_cap, \
        reset_display, _use_better_clock, _saved_dims, \
        is_init

    is_init = True

    params = Configs.merge_params(options, Configs.game_defaults)

    name = params["name"]
    window_size = params["window_size"]
    resolution = params["resolution"]

    fps_cap = params["fps_cap"]
    Time.fdt = params["physics_timestep"]
    reset_display = params["reset_display"]
    _use_better_clock = params["better_clock"]

    flags = (sdl2.SDL_WINDOW_RESIZABLE | sdl2.SDL_WINDOW_ALLOW_HIGHDPI)
    Display.window = sdl2.ext.Window(name, window_size.to_tuple(), flags=flags)

    Display.renderer = sdl2.ext.Renderer(
        Display.window.get_surface(),
        flags=(sdl2.SDL_RENDERER_ACCELERATED
               | sdl2.SDL_RENDERER_PRESENTVSYNC))

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
    global _saved_dims, _physics_count
    dnd_if_paused = get_state() != STATE.PAUSED
    # Event handling
    for event in sdl2.ext.get_events():
        sdl2.SDL_PumpEvents()
        if event.type == sdl2.SDL_QUIT:
            radio.broadcast("EXIT", {})
            sdl2.SDL_Quit()
            sys.exit(1)
        if event.type == sdl2.SDL_WINDOWEVENT_RESIZED:
            global window_size
            window_size = Vector.from_tuple(event.size)
        if event.type == sdl2.SDL_KEYDOWN:
            key_info = event.key.keysym
            radio.broadcast(
                "keydown",
                {
                    "key": Input.get_name(key_info.sym),
                    "unicode": chr(key_info.sym),
                    "code": int(key_info.sym),
                    "modifiers": key_info.mod,
                },
            )
        if event.type == sdl2.SDL_KEYUP:
            key_info = event.key.keysym
            radio.broadcast(
                "keydown",
                {
                    "key": Input.get_name(key_info.sym),
                    "unicode": chr(key_info.sym),
                    "code": int(key_info.sym),
                    "modifiers": key_info.mod,
                },
            )

    # Window resize handling
    # if (_saved_dims.x != window_size.x or _saved_dims.y != window_size.y):
    #     Display.screen = sdl2.surface.SDL_CreateRGBSurfaceWithFormat(
    #         0,
    #         window_size.x,
    #         window_size.y,
    #         64,
    #         sdl2.SDL_PIXELFORMAT_RGBA32,
    #     )

    # aspect_ratio = resolution.x / resolution.y
    # ratio = (window_size.x / window_size.y) < aspect_ratio
    # width = (window_size.y * aspect_ratio, window_size.x)[ratio]
    # height = (window_size.y, window_size.x / aspect_ratio)[ratio]
    # top_left = (((window_size.x - width) // 2, 0),
    #             (0, (window_size.y - height) // 2))[ratio]

    _saved_dims = window_size.clone()

    # Delayed calls handling
    if dnd_if_paused and get_state():
        Time.process_calls()

    # Fixed Update Loop
    _physics_count += Time.delta_time()

    _physics_count = Math.clamp(_physics_count, 0, Time.fdt * 100)

    while dnd_if_paused and _physics_count > Time.fdt:
        scenes.fixed_update()
        _physics_count -= Time.fdt

    # Regular Update Loop
    if dnd_if_paused:
        scenes.update()

    # Draw Loop
    if dnd_if_paused:
        sdl2.ext.draw.fill(Display.window.get_surface(), (0, 0, 0))
        if reset_display:
            Display.renderer.fill(
                (0, 0, Display.renderer.logical_size[0],
                 Display.renderer.logical_size[1]),
                0xFFFFFFFF,
            )
        scenes.draw()

    # Update Screen
    Display.window.refresh()
    Display.renderer.present()
    radio.events = []
    # if dnd_if_paused:
    #     if _use_better_clock:
    #         _clock.tick_busy_loop(fps_cap)
    #     else:
    #         _clock.tick(fps_cap)
    # else:
    #     sdl2.timer.SDL_Delay(int(Time.delta_time()))


def render(sprite: Sprite, surface: sdl2.surface.SDL_Surface):
    if sprite.z_index <= scenes.current_scene.camera.z_index:
        width, height = surface.w, surface.h

        new_size = (
            round(width * scenes.current_scene.camera.zoom),
            round(height * scenes.current_scene.camera.zoom),
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
            scenes.current_scene.camera.transform(
                Sprite.center_to_tl(sprite.pos, Vector(width, height)) *
                scenes.current_scene.camera.zoom),
        )


def get_state() -> STATE:
    return _state


def set_state(new_state: STATE):
    global _state
    _state = new_state

    if _state == STATE.STOPPED:
        sdl2.events.SDL_PushEvent(sdl2.events.SDL_QuitEvent())
