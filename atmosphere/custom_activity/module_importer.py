import importlib
from inspect import isclass

from .base_class import BaseActivityCustomCode
from .base_config import Config


def find_constructor_subclass(klass_name: str, file_path: str):
    module = importlib.import_module(file_path)
    attribute = getattr(module, klass_name)

    if not (
        isclass(attribute)
        and issubclass(attribute, BaseActivityCustomCode)
        and not issubclass(BaseActivityCustomCode, attribute)
    ):
        # Keep only the strict subclass of BaseCustomCode, not to add
        # BaseCustomCode to the list.
        raise ValueError(
            (
                f"Error getting the class {klass_name}'s constructor "
                "from the file {file_path}."
            )
        )
    return attribute


def get_module_constructor(config: Config):
    return find_constructor_subclass(config.class_name, config.module_file)
