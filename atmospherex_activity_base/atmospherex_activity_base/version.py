import re

from .base_config import ConfigError


def get_base_version_from_requirement_file(requirement_file_path: str) -> str:
    reg = r"git\+https\:\/\/git\@github\.com\/ambiata\/atmosphere-python-sdk\.git\@(.*)\#subdirectory=atmospherex_activity_base$"
    with open(requirement_file_path) as file:
        for line in file:
            match = re.search(reg, line.strip())
            if match:
                return match.group(1)

    raise ConfigError(
        f"Could not find the activity base library version from the given requirement file {requirement_file_path}.")
