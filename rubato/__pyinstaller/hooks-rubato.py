"""The PyInstaller hooks file for Rubato."""
from pathlib import Path
import rubato

rubato_path = Path(rubato.__file__).parent

datas = [
    (
        rubato_path / "static",
        "./rubato/static",
    ),
]
