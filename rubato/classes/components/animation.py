"""
Animations are a series of images that loop in a set loop
"""
from typing import List, Dict, TYPE_CHECKING
from os import path, walk
import sdl2
from rubato.classes import Component
from rubato.classes.components.image import Image
from rubato.utils import Defaults, Vector, Time

if TYPE_CHECKING:
    from rubato.classes import Spritesheet


class Animation(Component):
    """
    Made of a a dictionary holding the different states ie. running, idle, etc.
    each holding separate frames and their times.

    Attributes:
        rotation (float): The rotation of the animation.
        default_state (Union[str, None]): The key of the default state. Defaults
            to None.
        current_state (str): The key of the current state. Defaults to "".
        animation_frames_left (int): The number of animation frames left.
        loop (bool): Whether the animation should loop. Defaults to False.
        aa (bool): Whether or not to enable anti aliasing.
        flipx (bool): Whether or not to flip the image along the x axis
        flipy (bool): Whether or not to flip the image along the y axis
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
        self.default_state: str = None
        self.current_state: str = ""
        self.animation_frames_left: int = 0
        self._current_frame: int = 0
        self.loop = False
        self._scale = param["scale_factor"]
        self.aa: bool = param["anti_aliasing"]
        self.flipx: bool = param["flipx"]
        self.flipy: bool = param["flipy"]
        self.offset: Vector = param["offset"]

        # time (milliseconds) to switch frames
        self._time_step = 1000 / self._fps
        self._time_count = 0  # time since last update of frames

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
        """
        The current SDL Surface holding the image.
        """
        return self._states[self.current_state][self.current_frame].image

    @property
    def anim_frame(self) -> Image:
        """
        The current frame.
        """
        img = self._states[self.current_state][self.current_frame]
        img.aa = self.aa
        img.flipx = self.flipx
        img.flipy = self.flipy
        img.scale = self._scale
        img.offset = self.offset
        return img

    def scale(self, scale_factor: Vector):
        """
        Scales the Animation to the given scale factor.

        Args:
            scale_factor: The 2-d scale factor relative to it's current size.
        """
        self._scale = scale_factor

    def resize(self, new_size: Vector):
        """
        Resize the Animation to a given size in pixels.

        Args:
            new_size: The new size of the Animation in pixels.
        """
        for value in self._states.values():
            for anim_frame in value:
                anim_frame.resize(new_size)

    def set_current_state(self, new_state: str, loop: bool = False):
        """
        Set the current animation state.

        Args:
            new_state: The key of the new current state.
            loop: Whether to loop the state. Defaults to False.

        Raises:
            KeyError: The new_state key is not in the initialized states.
        """
        if new_state != self.current_state:
            if new_state in self._states:
                self.loop = loop
                self.current_state = new_state
                self.reset()
            else:
                raise KeyError(f"The given state {new_state} is not in the initialized states")

    def reset(self):
        """Reset the animation state back to frame 0"""
        self.current_frame = 0

    def add(self, state_name: str, images: List[Image]):
        """
        Adds a state to this animation component.

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
        Adds a state from an folder of images. Directory must be
        solely comprised of images.

        Args:
            state_name: The key used to reference this state.
            rel_path: The relative path to the folder you wish to import
        """
        ret_list = []
        for _, _, files in walk(rel_path):
            # walk to directory path and ignore name and subdirectories
            files.sort()
            for image_path in files:
                path_to_image = path.join(rel_path, image_path)
                image = Image({
                    "rel_path": path_to_image,
                })
                ret_list.append(image)

        self.add(state_name, ret_list)

    def add_spritesheet(self, state_name: str, spritesheet: "Spritesheet", from_coord: Vector, to_coord: Vector):
        """
        Adds a state from a spritesheet. Will include all sprites from the from_coord to the to_coord.

        Args:
            state_name: The key used to reference this state.
            spritesheet: The spritesheet to use.
            from_coord: The grid coordinate of the first frame.
            to_coord: The grid coordinate of the last coord.
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
        for images in self._states.values():
            for image in images:
                image.gameobj = self.gameobj

    def draw(self):
        self._time_count += Time.delta_time

        while self._time_count > self._time_step:
            self.anim_tick()
            self._time_count -= self._time_step

        self.anim_frame.draw()

    def anim_tick(self):
        """An animation processing tick"""
        if self.animation_frames_left > 0:
            # still frames left
            self.current_frame += 1
        elif self.loop:  # we reached the end of our state
            self.reset()
        else:
            self.set_current_state(self.default_state, True)

        self.anim_frame.rotation = self.rotation
