#!/bin/sh -e
set -x

python_packages="atmosphere tests"

# Remove unused imports
autoflake --ignore-init-module-imports --in-place -r --remove-all-unused-imports $python_packages
# Sort imports one per line, so autoflake can remove unused imports
autopep8 --in-place --aggressive --aggressive --recursive $python_packages
isort --force-single-line-imports $python_packages
# --exclude=__init__.py
black $python_packages
isort $python_packages
