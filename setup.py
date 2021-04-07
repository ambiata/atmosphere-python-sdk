import setuptools
import pathlib

current_dir = pathlib.Path(__file__).parent.absolute()

def get_version():
    with open(current_dir / "atmosphere" / "VERSION") as version_file:
        return version_file.readlines()[1].strip()

setuptools.setup(
    name="atmosphere",
    author="Ambiata",
    description="The atmosphere python SDK including multiple modules to help with setting up activities, transformers and more.",
    long_description_content_type="text/markdown",
    url="https://github.com/ambiata/atmosphere-python-sdk.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    version=get_version(),
    python_requires='>=3.6',
    install_requires=[
        'apscheduler>=3.6.3',
        'fastapi>=0.61.1',
        'pyyaml>=5.4.1',
        'requests>=2.24.0',
        'uvicorn>=0.11.8',
        'numpy>=1.19.2',
        'pydantic>=1.6.1',
        'seldon-core>=1.7.0',
        'simplejson>=3.17.2',
    ],
    tests_require=[
        'httpretty',
        'pytest',
        'pytest-cov',
        'pytest-env',
        'requests-mock==1.8.0',
    ]
)
