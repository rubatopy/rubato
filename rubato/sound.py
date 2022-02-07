"""
A fully functional, multi-channel sound system.
"""

from pygame import mixer

_loaded_sounds: dict[str, mixer.Sound] = {}


def loaded_sounds() -> dict[str, mixer.Sound]:
    """
    A dictionary of all the loaded sounds. The keys are the filename.

    Returns:
        dict[str, pygame.mixer.Sound]: The returned dictionary.
    """
    return _loaded_sounds
