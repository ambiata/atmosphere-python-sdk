import pathlib

import setuptools

current_dir = pathlib.Path(__file__).parent.absolute()


def get_version():
    with open(current_dir / "atmosphere" / "VERSION") as version_file:
        return version_file.readlines()[1].strip()


setuptools.setup(
    name="atmosphere",
    author="Ambiata",
    description="The atmosphere python SDK including multiple modules to help with setting up activities, "
                "transformers and more.",
    long_description_content_type="text/markdown",
    url="https://github.com/ambiata/atmosphere-python-sdk.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    version=get_version(),
    python_requires='>=3.8',
    install_requires=[
        'apscheduler>=3.9.1',
        'fastapi>=0.75.1',
        'PyJWT>=2.3.0',
        'simplejson>=3.17.6',
        'uvicorn>=0.17.6'
    ]
)
