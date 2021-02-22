#!/usr/bin/env bash
set -x

EXIT_STATUS=0

isort --recursive --check-only app || EXIT_STATUS=$?
pylint app || EXIT_STATUS=$?

exit $EXIT_STATUS
