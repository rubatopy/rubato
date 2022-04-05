"""
This is the animation component module for game objects.
"""
from __future__ import annotations
from typing import List, Dict, TYPE_CHECKING
from os import path, walk
import sdl2

from . import Component, Image
from ... import Defaults, Vector, Time

if TYPE_CHECKING:
    from . import Spritesheet


class Animation(Component):
    """
    Animations are a series of images that update automatically in accordance with parameters.

    Attributes:
        rotation (float): The rotation of the animation.
        default_state (Union[str, None]): The key of the default state. Defaults
            to None.
        current_state (str): The key of the current state. Defaults to "".
        animation_frames_left (int): The number of animation frames left.
        loop (bool): Whether the animation should loop. Defaults to False.
        aa (bool): Whether or not to enable anti aliasing.
        flipx (bool): Whether or not to flip the animation along the x axis.
        flipy (bool): Whether or not to flip the animation along the y axis.
        visible (bool): Whether or not the animation is visible.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes an Animation.

        Args:
            options: A Animation config. Defaults to the |default| for
                `Animation`.
        """
        param = Defaults.animation_defaults | options
        super().__init__()

        self.rotation = param["rotation"]
        self._fps: int = param["fps"]
        self.singular = False

        self._states: Dict[str, List[Image]] = {}
        self._freeze: int = -1

        self.default_state: str = None
        self.current_state: str = ""
        self.animation_frames_left: int = 0
        self._current_frame: int = 0
        self.loop = True
        self.scale = param["scale"]
        self.aa: bool = param["anti_aliasing"]
        self.flipx: bool = param["flipx"]
        self.flipy: bool = param["flipy"]
        self.offset: Vector = param["offset"]
        self.visible: bool = param["visible"]

        self._time_step = 1000 / self._fps
        self._time_count = 0

    @property
    def fps(self):
        """The fps of the animation."""
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps
        self._time_step = 1000 / self._fps

    @property
    def current_frame(self) -> int:
        """The current frame that the animation is on."""
        return self._current_frame

    @current_frame.setter
    def current_frame(self, new: int):
        self._current_frame = new
        self.animation_frames_left = len(self._states[self.current_state]) - (1 + self._current_frame)

    @property
    def image(self) -> sdl2.surface.SDL_Surface:
        """The current SDL Surface holding the image."""
        return self._states[self.current_state][self.current_frame].image

    @property
    def anim_frame(self) -> Image:
        """The current animation frame."""
        img = self._states[self.current_state][self.current_frame]
        img.aa = self.aa
        img.flipx = self.flipx
        img.flipy = self.flipy
        img.scale = self.scale
        img.offset = self.offset
        img.visible = self.visible
        return img

    def resize(self, new_size: Vector):
        """
        Resize the Animation to a given size in pixels.

        Args:
            new_size: The new size of the Animation in pixels.
        """
        for value in self._states.values():
            for anim_frame in value:
                anim_frame.resize(new_size)

    def set_current_state(self, new_state: str, loop: bool = False, freeze: int = -1):
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
            if new_state in self._states:
                self.loop = loop
                self.current_state = new_state
                self.reset()
                self._freeze = freeze
            else:
                raise KeyError(f"The given state {new_state} is not in the initialized states")

    def reset(self):
        """Reset the animation state back to the first frame."""
        self.current_frame = 0

    def add(self, state_name: str, images: List[Image]):
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

    def add_folder(self, state_name: str, rel_path: str):
        """
        Adds a state from a folder of images. Directory must be solely comprised of images.

        Args:
            state_name: The key used to reference this state.
            rel_path: The relative path to the folder you wish to import
        """
        ret_list = []
        for _, _, files in walk(rel_path):
            # walk to directory path and ignore name and subdirectories
            files.sort()
            for image_path in files:
                try:
                    path_to_image = path.join(rel_path, image_path)
                    image = Image({
                        "rel_path": path_to_image,
                    })
                    ret_list.append(image)
                except TypeError:
                    continue

        self.add(state_name, ret_list)

    def add_spritesheet(
        self, state_name: str, spritesheet: Spritesheet, from_coord: Vector = Vector(), to_coord: Vector = Vector()
    ):
        """
        Adds a state from a spritesheet. Will include all sprites from the from_coord to the to_coord.

        Args:
            state_name: The key used to reference this state.
            spritesheet: The spritesheet to use.
            from_coord: The grid coordinate of the first frame. Defaults to Vector().
            to_coord: The grid coordinate of the last coord. Defaults to Vector().
        Example:
            .. code-block:: python

                animation.add_spritesheet("idle", spritesheet, Vector(0, 0), Vector(1, 3))
                # This will add the frames (0, 0) to (0, size) and (1, 0) to (1, 3) inclusive to the animation
                # with the state name "idle".

                animation.add_spritesheet("idle", spritesheet, to_coord=spritesheet.end)
                # This will just load from the start to the end of the spritesheet.
        """
        state = []
        x = from_coord.x
        y = from_coord.y
        while True:
            state.append(spritesheet.get(x, y))
            if y == to_coord.y and x == to_coord.x:
                break
            x += 1
            if x >= spritesheet.grid_size.x:
                x = 0
                if y >= spritesheet.grid_size.y:
                    break
                y += 1

        self.add(state_name, state)

    def setup(self):
        """Sets up the animation component."""
        for images in self._states.values():
            for image in images:
                image.gameobj = self.gameobj

    def draw(self):
        """Draws the animation frame and steps the animation forward."""
        self._time_count += Time.delta_time

        while self._time_count > self._time_step:
            self.anim_tick()
            self._time_count -= self._time_step

        self.anim_frame.draw()

    def anim_tick(self):
        """An animation processing tick."""
        if self.current_frame != self._freeze:
            if self.animation_frames_left > 0:
                # still frames left
                self.current_frame += 1
            elif self.loop:  # we reached the end of our state
                self.reset()
            else:
                self.set_current_state(self.default_state, True)

        self.anim_frame.rotation = self.rotation

    def delete(self):
        """Deletes the animation component"""
        for state in self._states.values():
            for image in state:
                image.delete()
        self._states = {}
