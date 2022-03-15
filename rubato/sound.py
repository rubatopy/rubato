"""
A fully functional, multi-channel sound system.
"""

from os import path, walk
from typing import List, Dict, Union
import sdl2.sdlmixer as mixer
from rubato.utils.error import IdError

_loaded_sounds: Dict[str, List[Union[mixer.Mix_Chunk, int]]] = {}
# Loaded sounds are saved in the format:
# {sound_name: [sound_chunk, channel_id]}


def loaded_sounds() -> Dict[str, mixer.Mix_Chunk]:
    """
    A dictionary of all the loaded sounds. The keys are the filename.

    Returns:
        dict[str, sdl2.sdlmixer.Mix_Chunk]: The returned dictionary.
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
    sound = mixer.Mix_LoadWAV(bytes(rel_path, "utf-8"))

    _loaded_sounds[sound_name] = [sound, -1]


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
            import_sound(path_to_sound, sound_path.split(".")[0])


def get_sound(sound_name: str) -> mixer.Mix_Chunk:
    """
    Gets the sound based on the sound name.

    Args:
        sound_name: The name of the sound.

    Raises:
        IdError: No sound is associated to the sound name.

    Returns:
        sdl2.sdlmixer.Mix_Chunk: The sound.
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
    if mixer.Mix_GroupAvailable(-1) == -1:
        mixer.Mix_AllocateChannels(mixer.Mix_GroupCount(-1) + 1)

    channel = mixer.Mix_GroupAvailable(-1)

    mixer.Mix_PlayChannel(
        channel,
        get_sound(sound_name),
        loops,
    )

    _loaded_sounds[sound_name][1] = channel


# def stop_sound(sound_name: str):
#     """
#     Stops a sound.

#     Args:
#         sound_name: The name of the sound to stop.
#     """
#     get_sound(sound_name).stop()
