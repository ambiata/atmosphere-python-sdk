#!/usr/bin/env bash

set -e
set -x

pytest --cov=atmospherex_activity_base --cov-report=term-missing tests "${@}"
