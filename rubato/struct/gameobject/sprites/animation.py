"""
This is the animation component module for game objects.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from os import path as os_path, walk

from .. import Component
from .... import Vector, Time, get_path, Draw, Camera, Surface

if TYPE_CHECKING:
    from . import Spritesheet


class Animation(Component):
    """
    Animations are a series of images that update automatically in accordance with parameters.

    Args:
        scale: The scale of the animation. Defaults to (1, 1).
        fps: The frames per second of the animation. Defaults to 24.
        af: Whether to use anisotropic filtering on the animation. Defaults to False.
        flipx: Whether to flip the animation horizontally. Defaults to False.
        flipy: Whether to flip the animation vertically. Defaults to False.
        offset: The offset of the animation from the game object. Defaults to (0, 0).
        rot_offset: The rotation offset of the animation from the game object. Defaults to 0.
        z_index: The z-index of the animation. Defaults to 0.
        hidden: Whether the animation is hidden. Defaults to False.
    """

    def __init__(
        self,
        scale: Vector | tuple[float, float] = (1, 1),
        fps: int = 24,
        af: bool = False,
        flipx: bool = False,
        flipy: bool = False,
        offset: Vector | tuple[float, float] = (0, 0),
        rot_offset: float = 0,
        z_index: int = 0,
        hidden: bool = False,
    ):
        super().__init__(offset=offset, rot_offset=rot_offset, z_index=z_index, hidden=hidden)

        self._fps: int = fps
        self.singular = False

        self._states: dict[str, list[Surface]] = {}
        self._freeze: int = -1

        self.default_state: str = ""
        """The key of the default state."""
        self.current_state: str = ""
        """The key of the current state."""
        self.animation_frames_left: int = 0
        """The number of animation frames left."""
        self._current_frame: int = 0
        """The current frame of the animation."""
        self.loop: bool = True
        """Whether the animation should loop."""
        self.scale: Vector = Vector.create(scale)
        """The scale of the animation."""
        self.af: bool = af
        """Whether to enable anisotropic filtering."""
        self.flipx: bool = flipx
        """Whether to flip the animation along the x axis."""
        self.flipy: bool = flipy
        """Whether to flip the animation along the y axis."""

        self._time_step: float = 1 / self._fps
        self._time_count: float = 0

    @property
    def fps(self):
        """The fps of the animation."""
        return self._fps

    @fps.setter
    def fps(self, new):
        self._fps = new
        self._time_step = 1 / self._fps

    @property
    def current_frame(self) -> int:
        """The current frame that the animation is on."""
        return self._current_frame

    @current_frame.setter
    def current_frame(self, new: int):
        self._current_frame = new
        self.animation_frames_left = len(self._states[self.current_state]) - (1 + self._current_frame)

    def anim_frame(self) -> Surface:
        """The current animation frame."""
        surface = self._states[self.current_state][self.current_frame]
        surface.af = self.af
        surface.rotation = self.true_rotation()

        calculated_scale = self.scale.clone()
        if self.flipx:
            calculated_scale.x *= -1
        if self.flipy:
            calculated_scale.y *= -1

        surface.scale = calculated_scale
        if not surface.uptodate:
            surface.regen()
        return surface

    def set_state(self, new_state: str, loop: bool = False, freeze: int = -1):
        """
        Set the current animation state.

        Args:
            new_state: The key of the new current state.
            loop: Whether to loop the state. Defaults to False.
            freeze: Freezes the animation once the specified frame is reached (No animation).
                Use -1 to never freeze. Defaults to -1.

        Raises:
            KeyError: The new_state key is not in the initialized states.
        """
        if new_state != self.current_state:
            if new_state not in self._states:
                raise KeyError(f"The given state {new_state} is not in the initialized states")
            self.loop = loop
            self.current_state = new_state
            self.reset()
            self._freeze = freeze

    def reset(self):
        """Reset the animation state back to the first frame."""
        self.current_frame = 0

    def add(self, state_name: str, images: list[Surface]):
        """
        Adds a state to the animation.

        Args:
            state_name: The key used to reference this state.
            images: A list of images to use as the animation.
        """
        self._states[state_name] = images

        if len(self._states) == 1:
            self.default_state = state_name
            self.current_state = state_name
            self.reset()

    def add_folder(self, state_name: str, path: str, recursive: bool = True):
        """
        Adds a state from a folder of images. Directory must be solely comprised of images.

        Args:
            state_name: The key used to reference this state.
            path: The relative path to the folder you wish to import
            recursive: Whether it will import an animation shallowly or recursively. Defaults to True.
        """
        ret_list = []
        p = get_path(path)
        if not recursive:
            _, _, files = next(walk(p))
            files.sort()
            for image_path in files:
                try:
                    path_to_image = os_path.join(p, image_path)
                    image = Surface.from_file(path_to_image)
                    ret_list.append(image)
                except TypeError:
                    continue
        else:
            for _, _, files in walk(p):
                # walk to directory path and ignore name and subdirectories
                files.sort()
                for image_path in files:
                    try:
                        path_to_image = os_path.join(p, image_path)
                        image = Surface.from_file(path_to_image)
                        ret_list.append(image)
                    except TypeError:
                        continue

        self.add(state_name, ret_list)

    def add_spritesheet(
        self,
        state_name: str,
        spritesheet: Spritesheet,
        from_coord: Vector | tuple[float, float] = (0, 0),
        to_coord: Vector | tuple[float, float] = (0, 0)
    ):
        """
        Adds a state from a spritesheet. Will include all sprites from the from_coord to the to_coord.

        Args:
            state_name: The key used to reference this state.
            spritesheet: The spritesheet to use.
            from_coord: The grid coordinate of the first frame. Defaults to (0, 0).
            to_coord: The grid coordinate of the last coord. Defaults to (0, 0).

        Example:
            .. code-block:: python

                animation.add_spritesheet("idle", spritesheet, Vector(0, 0), Vector(1, 3))
                # This will add the frames (0, 0) to (0, size) and (1, 0) to (1, 3) inclusive to the animation
                # with the state name "idle".

                animation.add_spritesheet("idle", spritesheet, to_coord=spritesheet.end)
                # This will just load from the start to the end of the spritesheet.
        """
        state = []
        x, y = int(from_coord[0]), int(from_coord[1])
        to_x, to_y = int(to_coord[0]), int(to_coord[1])
        while True:
            state.append(spritesheet.get(x, y))
            if y == to_y and x == to_x:
                break
            x += 1
            if x >= spritesheet.grid_size.x:
                x = 0
                if y >= spritesheet.grid_size.y:
                    break
                y += 1

        self.add(state_name, state)

    def draw(self, camera: Camera):
        """Draws the animation frame and steps the animation forward."""

        self._time_count += Time.delta_time

        while self._time_count > self._time_step:
            self.anim_tick()
            self._time_count -= self._time_step

        Draw.queue_surface(self.anim_frame(), self.true_pos(), self.true_z(), camera)

    def anim_tick(self):
        """An animation processing tick."""
        if self.current_frame != self._freeze:
            if self.animation_frames_left > 0:
                # still frames left
                self.current_frame += 1
            elif self.loop:  # we reached the end of our state
                self.reset()
            else:
                self.set_state(self.default_state, True)

    def clone(self) -> Animation:
        """Clones the animation."""
        new = Animation(
            scale=self.scale.clone(),
            fps=self.fps,
            af=self.af,
            flipx=self.flipx,
            flipy=self.flipy,
            offset=self.offset.clone(),
            rot_offset=self.rot_offset,
            z_index=self.z_index,
        )

        new._states = self._states
        new.default_state = self.default_state
        new.current_state = self.current_state
        new.loop = self.loop
        new.current_frame = self.current_frame
        new._freeze = self._freeze
        return new
