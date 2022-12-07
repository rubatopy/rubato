"""The PyInstaller hooks file for rubato."""  # pylint: disable=invalid-name
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = collect_data_files("rubato")
datas += collect_data_files("sdl2dll")

hiddenimports = [
    "sdl2",
    "sdl2.sdlttf",
    "sdl2.ext",
    "sdl2.sdlmixer",
    "sdl2dll",
    "Cython",
    "pytiled_parser",
]
hiddenimports += collect_submodules("rubato")
