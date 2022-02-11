"""
Animations are a series of images that loop in a set loop
"""
from typing import List, Tuple, Dict
from os import path, walk

from pygame import Surface
from rubato.sprite.sprite import Component
from rubato.sprite.components.image import Image
from rubato.utils import Error, Configs, Vector


class Animation(Component):
    """
    Made of a a dictionary holding the different states ie. running, idle, etc.
    each holding separate frames and their times.

    Attributes:
        rotation (float): The rotation of the animation.
        default_animation_length (int): The default length of an animation in
            frames.
        default_state (Union[str, None]): The key of the default state. Defaults
            to None.
        current_state (str): The key of the current state. Defaults to "".
        animation_frames_left (int): The number of animation frames left.
        current_frame (int): The current frame of the animation.
        loop (bool): Whether the animation should loop. Defaults to False.
    """
    _IMAGE_INDEX = 0
    _TIME_INDEX = 1

    def __init__(self, options: dict = {}):
        """
        Initializes an Animation.

        Args:
            options: A Animation config. Defaults to the |default| for
                `Animation`.
        """
        param = Configs.merge_params(options, Configs.animation_defaults)
        super().__init__()

        self.rotation = param["rotation"]
        self.default_animation_length = param["default_animation_length"]
        self._states: Dict[str, List[Tuple[Image, int]]] = {}
        self.default_state: str = None
        self.current_state: str = ""
        self.animation_frames_left: int = 0
        self.current_frame: int = 0
        self.loop = False

        self.scale(param["scale_factor"])

    @property
    def image(self) -> Surface:
        """
        The current image.

        Returns:
            Surface: The pygame surface holding the current image.
        """
        return self._states[self.current_state][self.current_frame][
            Animation._IMAGE_INDEX].image

    @property
    def anim_frame(self) -> Image:
        """
        The current frame.

        Returns:
            Image: The image representing the current frame.
        """
        return self._states[self.current_state][self.current_frame][
            Animation._IMAGE_INDEX]

    @property
    def _current(self):
        return self._states[self.current_state][self.current_frame]

    def scale(self, scale_factor: Vector):
        """
        Scales the Images to the given scale factor.

        Args:
            scale_factor: The 2-d scale factor relative to it's current size.
        """
        for _, value in self._states:
            for anim_frame, _ in value:
                anim_frame.scale(scale_factor)

    def resize(self, new_size: Vector):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        for value in self._states.values():
            for anim_frame, _ in value:
                anim_frame.resize(new_size)

    def set_current_state(self, new_state: str, loop: bool = False):
        """
        Set the current animation state.

        Args:
            new_state: The key of the new current state.
            loop: Whether or not to loop the state. Defaults to False.

        Raises:
            KeyError: The new_state key is not in the initialized states.
        """
        if self.current_state == new_state:
            self.loop = loop
            return
        if new_state in self._states:
            self.loop = loop
            self.current_state = new_state
            self.current_frame = 0
            self.animation_frames_left = self._current[Animation._TIME_INDEX]
        else:
            raise KeyError(
                f"The given state {new_state} is not in the initialized states"
            )

    def add_state(self, state_name: str, image_and_times: List[tuple] | list):
        """
        Initializes a state to this animation component.

        Args:
            state_name: The key used to reference this state.
            image_and_times: The list of images and times. Should be the output
                of the ``import_animation_folder`` function or a list containing
                tuples following the format: (Image, frame_number)

        Raises:
            Error: The animation frame tuple is invalid.
        """
        for i in range(len(image_and_times)):
            image_and_time = image_and_times[i]
            if isinstance(image_and_time, Image):
                image_and_time.sprite = self.sprite
                image_and_times[i] = (image_and_time,
                                      self.default_animation_length)
            elif len(image_and_time) == 2 and \
                    isinstance(image_and_time[0], Image) \
                    and isinstance(image_and_time[1], int):
                image_and_time[0].sprite = self.sprite
            else:
                raise Error("This tuple is an invalid Image and time: " +
                            image_and_time)
        self._states[state_name] = image_and_times
        if len(self._states) == 1:
            self.default_state = state_name
            self.current_state = state_name

    def update(self):
        if self.current_frame < (length :=
                                 len(self._states[self.current_state]) - 1):
            # still in the state (extra -1 as we add if we hit a new frame)
            if self.animation_frames_left <= 0:
                self.current_frame += 1
                if self.current_frame >= length:
                    return self.update()
                self.animation_frames_left = self._current[
                    Animation._TIME_INDEX]
            self.animation_frames_left -= 1
        elif self.loop:  # we reached the end of our state
            self.current_frame = 0
            self.update()
        else:
            self.current_state = self.default_state
            self.current_frame = 0

        self.anim_frame.set_rotation(self.rotation)
        self.anim_frame.draw()

    @staticmethod
    def import_animation_folder(rel_path: str) -> list:
        """
        Imports a folder of images, creating rubato.Image for each one and
        placing it in a list by order in directory. Directory must be
        solely comprised of images.

        Args:
            rel_path: The relative path to the folder you wish to import

        Returns:
            list: a list of rubato.Image s. Filled with all images in
            given directory.
        """
        ret_list = []
        for _, _, files in walk(rel_path):
            # walk to directory path and ignore name and subdirectories
            for image_path in files:
                path_to_image = path.join(rel_path, image_path)
                image = Image({
                    "image_location": path_to_image,
                })
                ret_list.append(image)
        return ret_list
