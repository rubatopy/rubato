"""The PyInstaller hooks file for Rubato."""  # pylint: disable=invalid-name
from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files("rubato")
