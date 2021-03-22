import pathlib

current_dir = pathlib.Path(__file__).parent.absolute()


def get_version():
    with open(current_dir / "VERSION") as version_file:
        return version_file.readlines()[1].strip()


__version__ = get_version()
