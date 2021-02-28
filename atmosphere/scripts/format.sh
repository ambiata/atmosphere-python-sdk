#!/bin/sh -e
set -x

# Remove unused imports
autoflake --ignore-init-module-imports --in-place -r --remove-all-unused-imports .
# Sort imports one per line, so autoflake can remove unused imports
autopep8 --in-place --aggressive --aggressive --recursive .
isort --recursive  --force-single-line-imports --apply .
# --exclude=__init__.py
black .
isort --recursive --apply .
