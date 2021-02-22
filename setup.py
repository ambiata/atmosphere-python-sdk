import setuptools
from atmosphere._version import get_version

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
        'pyyaml>=5.3.1',
        'requests>=2.24.0',
        'uvicorn>=0.11.8',
        'numpy>=1.19.2',
        'pydantic>=1.6.1',
        'seldon-core>=1.3.0',
    ],
    tests_require=[
        'httpretty',
        'pytest',
        'pytest-cov',
        'pytest-env'
    ]
)
