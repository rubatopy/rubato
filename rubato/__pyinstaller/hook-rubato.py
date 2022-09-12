"""The PyInstaller hooks file for rubato."""  # pylint: disable=invalid-name
from PyInstaller.utils.hooks import collect_data_files

datas = [*collect_data_files("rubato"), *collect_data_files("sdl2dll")]
