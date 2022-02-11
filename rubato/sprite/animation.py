"""
Animations are a series of images that loop in a set loop
"""
from typing import List, Tuple, Dict

from rubato.scenes import Camera
from rubato.utils import Error, Configs, Vector
from pygame.image import load
from pygame.transform import scale, flip, rotate
from os import path, walk
from rubato.sprite.sprite import Sprite


class AnimationFrame:
    """
    A subclass of Sprite that handles Images.

    Attributes:
        image (pygame.Surface): The pygame surface containing the image.
    """

    def __init__(self, options: dict = {}):
        """
        Initializes an AnimationFrame
        Args:
            options: A AnimationFrame config. Defaults to the |default| for
                    `AnimationFrame`.
        """
        param = Configs.merge_params(options, Configs.animation_frame_defaults)

        if param["image_location"] in ["", "default"]:
            self.image = load("rubato/static/default.png").convert_alpha()
        elif param["image_location"] == "empty":
            self.image = load("rubato/static/empty.png").convert_alpha()
        else:
            self.image = load(param["image_location"]).convert_alpha()
        self.original = self.image.copy()
        self.rotation = param["rotation"]

    def get_size(self):
        return self.image.get_size()

    def get_size_original(self):
        return self.original.get_size()

    def set_rotation(self, angle):
        if self.rotation != angle:
            self.image = rotate(self.original, angle)
        self.rotation = angle

    def scale(self, scale_factor: Vector):
        """
        Scales the image.

        Args:
            scale_factor: The 2-d scale factor relative to it's current size.
        """
        if abs(new_x := self.image.get_width() * scale_factor.x) < 1:
            new_x = 1
        if abs(new_y := self.image.get_height() * scale_factor.y) < 1:
            new_y = 1
        self.image = flip(scale(self.original, (abs(new_x), abs(new_y))),
                          new_x < 0, new_y < 0)

    def resize(self, new_size: Vector):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        if abs(new_size.x) < 1:
            new_size.x = 1
        if abs(new_size.y) < 1:
            new_size.y = 1
        self.image = flip(
            scale(self.image, (abs(new_size.x), abs(new_size.y))),
            new_size.x < 0, new_size.y < 0)


class Animation(Sprite):
    """
    Made of a a dictionary holding the different states ie. running, idle, etc.
    each holding separate frames and their times. NOTE: ROTATION DOES NOT WORK!
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
        super().__init__({"pos": param["pos"], "z_index": param["z_index"]})

        self.rotation = param["rotation"]
        self.default_animation_length = param["default_animation_length"]
        self.states: Dict[str, List[Tuple[AnimationFrame, int]]] = {}
        self.default_state: str = None
        self.current_state: str = ""
        self.animation_frames_left: int = 0
        self.current_frame: int = 0
        self.loop = False
        self.scale(param["scale_factor"])

    @property
    def image(self):
        return self.states[self.current_state][self.current_frame][Animation._IMAGE_INDEX].image

    @property
    def anim_frame(self):
        return self.states[self.current_state][self.current_frame][Animation._IMAGE_INDEX]

    @property
    def _current(self):
        return self.states[self.current_state][self.current_frame]

    def scale(self, scale_factor: Vector):
        """
        Scales the AnimationFrames to the given scale factor.

        Args:
            scale_factor: The 2-d scale factor relative to it's current size.
        """
        for _, value in self.states:
            for anim_frame, _ in value:
                anim_frame.scale(scale_factor)

    def resize(self, new_size: Vector):
        """
        Resize the image to a given size in pixels.

        Args:
            new_size: The new size of the image in pixels.
        """
        for value in self.states.values():
            for anim_frame, _ in value:
                anim_frame.resize(new_size)

    def set_current_state(self, new_state, loop: bool = False):
        if self.current_state == new_state:
            self.loop = loop
            return
        if new_state in self.states:
            self.loop = loop
            self.current_state = new_state
            self.current_frame = 0
            self.animation_frames_left = self._current[Animation._TIME_INDEX]
        else:
            raise Error(
                f"The given state {new_state} is not in the given states")

    def add_state(self, state_name: str, image_and_times: list[tuple] | list):
        for i in range(len(image_and_times)):
            image_and_time = image_and_times[i]
            if isinstance(image_and_time, AnimationFrame):
                image_and_times[i] = (image_and_time, self.default_animation_length)
            elif len(image_and_time) == 2 and isinstance(image_and_time[0], AnimationFrame) \
                    and isinstance(image_and_time[1], int):
                pass
            else:
                raise Error(
                    f"this tuple is an invalid AnimationFrame and time: {image_and_time}")
        self.states[state_name] = image_and_times
        if len(self.states) == 1:
            self.default_state = state_name
            self.current_state = state_name

    def update(self):
        if self.current_frame < (length := len(self.states[self.current_state]) - 1):
            # still in the state (extra -1 as we add if we hit a new frame)
            if self.animation_frames_left <= 0:
                self.current_frame += 1
                if self.current_frame >= length:
                    return self.update()
                self.animation_frames_left = self._current[Animation._TIME_INDEX]
            self.animation_frames_left -= 1
        elif self.loop:  # we reached the end of our state
            self.current_frame = 0
            self.update()
        else:
            self.current_state = self.default_state
            self.current_frame = 0

    def draw(self, camera: Camera):
        """
        Draws the image if the z index of the current sprite is below the camera's.

        Args:
            camera: The current Camera viewing the scene.
        """
        self.anim_frame.set_rotation(self.rotation)
        super().draw(self.anim_frame.image, camera)

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
                image = AnimationFrame({
                    "image_location": path_to_image,
                })
                ret_list.append(image)
        return ret_list
