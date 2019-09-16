#!/usr/bin/env bash

set -euo pipefail

. ./venv/bin/activate

echo mypy...
mypy . 

echo lint...
./lint.sh --disable=fixme

echo pytest...
pytest --quiet
