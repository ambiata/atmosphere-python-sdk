import setuptools

setuptools.setup(
    name="atmospherex-activity-base",
    author="Ambiata",
    description="Base custom code templator.",
    long_description_content_type="text/markdown",
    url="https://github.com/ambiata/atmosphere-python-sdk.git#subdirectory=atmospherex-activity-base",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'apscheduler>=3.6.3',
        'fastapi>=0.61.1',
        'pyyaml>=5.3.1',
        'requests>=2.24.0',
        'uvicorn>=0.11.8'
    ],
    tests_require=[
        'httpretty',
        'pytest',
        'pytest-cov',
        'pytest-env'
    ]
)
