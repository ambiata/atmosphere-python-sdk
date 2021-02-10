#!/usr/bin/env bash

set -e
set -x

pytest -v --cov=atmospherex_transformer_base --cov-report=term-missing tests "${@}"
