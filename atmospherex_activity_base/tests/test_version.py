from tempfile import NamedTemporaryFile

import pytest

from atmospherex_activity_base.version import ConfigError, get_base_version_from_requirement_file


def test_get_version_from_requirement_file():
    version = "v0.0.24"
    string_test = f"""
    git+ssh://git@github.com/ambiata/atmospherex.git@{version}#subdirectory=atmospherex_activity_base
    click==7.1.2
    fastapi==0.61.1
    h11==0.9.0
    httptools==0.1.1
    pydantic==1.6.1
    starlette==0.13.6
    uvicorn==0.11.8
    uvloop==0.14.0
    websockets==8.1
    """
    with NamedTemporaryFile(mode='w+t', delete=False) as file:
        file.write(string_test)
        name = file.name
    obtained_version = get_base_version_from_requirement_file(name)

    assert obtained_version == version


def test_get_version_from_requirement_file_version_not_present():
    string_test = f"""
    click==7.1.2
    fastapi==0.61.1
    h11==0.9.0
    httptools==0.1.1
    pydantic==1.6.1
    starlette==0.13.6
    uvicorn==0.11.8
    uvloop==0.14.0
    websockets==8.1
    """
    with NamedTemporaryFile(mode='w+t', delete=False) as file:
        file.write(string_test)
        name = file.name
    with pytest.raises(ConfigError):
        get_base_version_from_requirement_file(name)


def test_get_version_from_requirement_file_file_not_present():
    with pytest.raises(FileNotFoundError):
        get_base_version_from_requirement_file("UNKNOWN.txt")
