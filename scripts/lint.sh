#!/usr/bin/env bash
set -x

EXIT_STATUS=0
python_packages="atmosphere tests"

isort --recursive --check-only atmosphere $python_packages || EXIT_STATUS=$?
pylint atmosphere $python_packages || EXIT_STATUS=$?

exit $EXIT_STATUS
