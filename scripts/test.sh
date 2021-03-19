#!/usr/bin/env bash

set -e
set -x

pytest --cov=atmosphere --cov-report=term-missing "${@}"
