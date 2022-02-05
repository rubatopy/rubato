"""
Animations are a series of images that loop in a set loop
"""
from rubato import Camera
from rubato.utils import Error, Configs
from rubato.sprite.image import Image
from rubato.sprite.sprite import Sprite


class Animation(Sprite):
    _IMAGE_INDEX = 0
    _TIME_INDEX = 1

    def __init__(self, options: dict = {}):
        """
        Initializes an Animation.

        Args:
            options: A sprite config. Defaults to the |default| for
                `Animation`.
        """
        param = Configs.merge_params(options, Configs.sprite_defaults)
        super().__init__({"pos": param["pos"], "z_index": param["z_index"]})
        self.states: dict = {}
        self.default_state: str = None
        self.current_state: str = ""
        self.animation_frames_left: int = 0
        self.current_frame: int = 0
        self.loop = False

    @property
    def _current(self):
        return self.states[self.current_state][self.current_frame]

    def set_current_state(self, new_state, loop: bool = False):
        self.loop = loop
        if new_state in self.states:
            self.current_state = new_state
            self.current_frame = 0
            self.animation_frames_left = self._current[Animation._TIME_INDEX]
        else:
            raise Error(
                f"The given state {new_state} is not in the given states")

    def add_state(self, state_name: str, image_and_times: list[tuple]):
        for i in range(len(image_and_times)):
            image_and_time = image_and_times[i]
            if len(image_and_time) == 1 and isinstance(image_and_time[0], Image):
                image_and_times[i] = (image_and_time[0], 5)
            elif len(image_and_time) == 2 and isinstance(image_and_time[0], Image) \
                    and isinstance(image_and_time[1], int):
                pass
            else:
                raise Error(
                    f"this tuple is an invalid image and time: {image_and_time}")
        self.states[state_name] = image_and_times
        if len(self.states) == 1:
            self.default_state = state_name

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
        super().draw(self._current[Animation._IMAGE_INDEX], camera)
