#!/bin/sh -e
set -x

# Remove unused imports
autoflake --ignore-init-module-imports --in-place -r --remove-all-unused-imports atmosphere
# Sort imports one per line, so autoflake can remove unused imports
autopep8 --in-place --aggressive --aggressive --recursive atmosphere
isort --recursive  --force-single-line-imports --apply atmosphere
# --exclude=__init__.py
black atmosphere
isort --recursive --apply atmosphere
