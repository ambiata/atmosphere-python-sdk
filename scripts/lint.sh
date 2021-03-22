#!/usr/bin/env bash
set -x

EXIT_STATUS=0
python_packages="atmosphere tests"

isort --check-only $python_packages || EXIT_STATUS=$?
pylint $python_packages || EXIT_STATUS=$?

exit $EXIT_STATUS
