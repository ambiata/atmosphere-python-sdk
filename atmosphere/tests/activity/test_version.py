from tempfile import NamedTemporaryFile

import pytest

from atmosphere.activity.version import ConfigError, get_base_version


def test_get_version():
    """
    Test whether the version is picked up frm an importlib version check.
    Not sure yet if there is a good way to test this within here.
    Our old test was just testing a regex.
    """
    pass
