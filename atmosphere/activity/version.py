import re
from importlib.metadata import version

from .base_config import ConfigError


def get_base_version(requirement_file_path: str) -> str:
    """ Use importlib to figure out what version of atmosphere we use """
    return version('atmosphere')
