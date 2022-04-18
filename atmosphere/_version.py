import pathlib
from sys import getdefaultencoding

current_dir = pathlib.Path(__file__).parent.absolute()


def get_version():
    with open(current_dir / "VERSION", encoding=getdefaultencoding()) as version_file:
        return version_file.readlines()[1].strip()


__version__ = get_version()
