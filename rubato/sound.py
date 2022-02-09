"""
A fully functional, multi-channel sound system.
"""

from os import path, walk
from pygame import mixer

from rubato.utils.error import IdError

_loaded_sounds: dict[str, mixer.Sound] = {}


def loaded_sounds() -> dict[str, mixer.Sound]:
    """
    A dictionary of all the loaded sounds. The keys are the filename.

    Returns:
        dict[str, pygame.mixer.Sound]: The returned dictionary.
    """
    return _loaded_sounds


def import_sound(rel_path: str, sound_name: str):
    """
    Imports a sound and saves it in the loaded_sounds dictionary with the key
    being the sound_name.

    Args:
        rel_path: The relative path to the sound file you wish to import.
        sound_name: The name of the sound.
    """
    sound = mixer.Sound(rel_path)

    _loaded_sounds[sound_name] = sound


def import_sound_folder(rel_path: str):
    """
    Imports a folder of sounds, saving each one in the loaded_sounds
    dictionary by filename.

    Args:
        rel_path: The relative path to the folder you wish to import.
    """
    for _, _, files in walk(rel_path):
        # walk to directory path and ignore name and subdirectories
        for sound_path in files:
            path_to_sound = path.join(rel_path, sound_path)
            _loaded_sounds[sound_path.split(".")[0]] = mixer.Sound(
                path_to_sound)


def get_sound(sound_name: str) -> mixer.Sound:
    """
    Gets the sound based on the sound name.

    Args:
        sound_name: The name of the sound.

    Raises:
        IdError: No sound is associated to the sound name.

    Returns:
        mixer.Sound: The sound.
    """
    try:
        return _loaded_sounds[sound_name]
    except KeyError as e:
        raise IdError(f"No sound with the name {sound_name} found") from e


def play_sound(sound_name: str, loops: int = 0):
    """
    Plays a sound.

    Args:
        sound_name: The name of the sound to play.
        loops: The number of times to loop a sound after the first play through.
            Use -1 to loop forever. Defaults to 0.
    """
    if mixer.find_channel() is None:
        mixer.set_num_channels(mixer.get_num_channels() + 1)

    get_sound(sound_name).play(loops)


def stop_sound(sound_name: str):
    """
    Stops a sound.

    Args:
        sound_name: The name of the sound to stop.
    """
    get_sound(sound_name).stop()
