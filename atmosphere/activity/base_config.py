import os

CLASS_NAME_ENV_VAR_KEY = 'CLASS_NAME'
MODULE_ENV_VAR_KEY = 'MODULE'


class ConfigError(Exception):
    pass


class Config:
    def __init__(self):
        self.class_name = os.getenv(CLASS_NAME_ENV_VAR_KEY)
        self.module_file = os.getenv(MODULE_ENV_VAR_KEY)

        if not self.class_name or not self.module_file:
            raise ValueError(
                f"The environment variables {CLASS_NAME_ENV_VAR_KEY} and/or {MODULE_ENV_VAR_KEY} have not been "
                f"provided."
            )
