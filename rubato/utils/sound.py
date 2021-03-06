"""
A fully functional, multi-channel sound system.
"""
from __future__ import annotations
from os import path, walk
from typing import Dict
from ctypes import c_int, CFUNCTYPE

import sdl2.sdlmixer as mixer
from sdl2 import AUDIO_F32

from . import IdError, get_path, Math


if mixer.Mix_OpenAudio(48000, AUDIO_F32, 2, 2048):
    raise Exception("Could not open audio device.")


@CFUNCTYPE(None, c_int)
def channel_finish_callback(channel_num: int):
    sound = Sound.active_channels.pop(channel_num)
    sound.channels &= ~(2**channel_num)


mixer.Mix_ChannelFinished(channel_finish_callback)


class Sound():
    """
    A sound class that is used to manage the sounds throughout the project. We support the following audio formats:
        * MP3
        * WAV
        * OGG
        * FLAC
        * MOD
        * MIDI (not always available on linux)
        * OPUS
        * AIFF
        * VOC

    Args:
        rel_path: The relative path to the sound file you wish to import.
        sound_name: The name of the sound. Defaults to the name of the file.

    Attributes:
        loaded_sounds (Dict[str, Sound]): A dictionary housing all the loaded
            sounds, stored by their name.
        active_channels (Dict[int, Sound]): A dictionary housing all the active sounds, stored by their name.
    """
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

    loaded_sounds: Dict[str, Sound] = {}
    active_channels: Dict[int, Sound] = {}

    def __init__(self, rel_path: str, sound_name: str = None):
        self.chunk = mixer.Mix_LoadWAV(rel_path.encode("utf-8"))
        self.channels = 0
        self._paused = False
        self._volume = int(mixer.MIX_MAX_VOLUME / 2)

        if not sound_name:
            self.name = rel_path.split("/")[-1].split(".")[0]
        else:
            self.name = sound_name

        if self.name in Sound.loaded_sounds:
            mixer.Mix_FreeChunk(self.chunk)
            raise IdError(f"There is already a sound with the name {self.name}")
        else:
            Sound.loaded_sounds[self.name] = self

    @property
    def state(self) -> int:
        """
        The current state of the sound.

        The possible states are::

            Sound.STOPPED
            Sound.PLAYING
            Sound.PAUSED

        Returns:
            int: The current state of the sound.
        """
        if not self.channels:
            return self.STOPPED
        elif self._paused:
            return self.PAUSED
        else:
            return self.PLAYING

    def play(self, loops: int = 0, init_volume: int = None):
        """
        Plays a sound.

        Args:
            loops: The number of times to loop a sound after the first play
                through. Use -1 to loop forever. Defaults to 0.'
            init_volume: The initail volume of the sound. Defaults to the volume of the sound.
                range(0, MIX_MAX_VOLUME=>128)
        """
        channel: int = mixer.Mix_PlayChannel(-1, self.chunk, loops)

        if channel == -1:
            mixer.Mix_AllocateChannels(mixer.Mix_AllocateChannels(-1) + 1)
            channel: int = mixer.Mix_PlayChannel(-1, self.chunk, loops)

        if self._paused:
            mixer.Mix_Pause(channel)

        Sound.active_channels[channel] = self
        self.channels |= 2**channel

        if init_volume:
            self._volume = init_volume
        self.set_volume(self._volume)

    def stop(self):
        """
        Stops all instances of the sound.
        """
        for i in range(self.channels.bit_count()):
            if self.channels & (1 << i):
                mixer.Mix_HaltChannel(i)
                if not self.channels:
                    return

    def pause(self):
        """
        Pauses all instances of the sound.
        """
        for i in range(self.channels.bit_count()):
            if self.channels & (1 << i):
                mixer.Mix_Pause(i)
        self._paused = True

    def resume(self):
        """
        Resumes all instance of the sound.
        """
        for i in range(self.channels.bit_count()):
            if self.channels & (1 << i):
                mixer.Mix_Resume(i)
        self._paused = False

    def set_volume(self, volume: int):
        """
        Sets the volume of the sound.

        Args:
            volume: The volume of the sound. range(0, MIX_MAX_VOLUME=>128)
        """
        self._volume = int(Math.clamp(volume, 0, mixer.MIX_MAX_VOLUME))
        mixer.Mix_VolumeChunk(self.chunk, c_int(self._volume))

    def get_volume(self) -> int:
        """
        Gets the volume of the sound.

        Returns:
            The volume of the sound. range(0, MIX_MAX_VOLUME=>128)
        """
        return self._volume

    @classmethod
    def import_sound_folder(cls, rel_path: str, duplicate_names=False, recursive: bool = True):
        """
        Imports a folder of sounds, saving each one in the loaded_sounds
        dictionary by filename.

        Args:
            rel_path: The relative path to the folder you wish to import.
            duplicate_names: if you wish to have duplicate names to your sounds,
            it will use the relative and the sound path for the sounds name
            recursive: Whether it will import an animation shallowly or recursively. Defaults to True.
        """
        p = get_path(rel_path)

        if not recursive:
            _, _, files = next(walk(p))
            # walk to directory path and ignore name and subdirectories
            for sound_path in files:
                path_to_sound = path.join(p, sound_path)
                name = (p + sound_path).split(".")[0] if duplicate_names else sound_path.split(".")[0]
                try:
                    cls(path_to_sound, name)
                except IdError as err:
                    raise Warning("If you have files with duplicate names you must set duplicate_names"
                                  "to True") from err
        else:
            for _, _, files in walk(p):
                # walk to directory path and ignore name and subdirectories
                for sound_path in files:
                    path_to_sound = path.join(p, sound_path)
                    name = (rel_path + "/" + sound_path).split(".")[0] if duplicate_names else sound_path.split(".")[0]
                    try:
                        cls(path_to_sound, name)
                    except IdError as err:
                        raise Warning("If you have files with duplicate names you must set duplicate_names"
                                      "to True") from err

    @classmethod
    def get_sound(cls, sound_name: str) -> Sound:
        """
        Gets the sound based on the sound name.

        Args:
            sound_name: The name of the sound.

        Raises:
            IdError: No sound is associated to the sound name.

        Returns:
            Sound: The sound.
        """
        try:
            return cls.loaded_sounds[sound_name]
        except KeyError as e:
            raise IdError(f"No sound with the name {sound_name} found") from e
