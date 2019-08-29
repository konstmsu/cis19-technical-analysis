#!/usr/bin/env bash

set -euo pipefail

. ./venv/bin/activate
pytest --quiet
mypy . 
./lint.sh