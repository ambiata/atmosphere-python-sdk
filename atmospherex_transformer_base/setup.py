import setuptools

setuptools.setup(
    name="atmospherex-transformer-base",
    author="Ambiata",
    description="Base atmosphere transformer templator.",
    long_description_content_type="text/markdown",
    url="https://github.com/ambiata/atmospherex.git#subdirectory=atmospherex-transformer-base",
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.19.2',
        'pydantic>=1.6.1',
        'seldon-core>=1.3.0',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-env'
    ]
)
