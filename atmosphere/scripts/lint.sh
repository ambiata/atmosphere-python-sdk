#!/usr/bin/env bash
set -x

EXIT_STATUS=0

isort --recursive --check-only app || EXIT_STATUS=$?
pylint activity || EXIT_STATUS=$?
pylint transformer || EXIT_STATUS=$?

exit $EXIT_STATUS
