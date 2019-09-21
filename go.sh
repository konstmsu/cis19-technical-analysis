#!/usr/bin/env bash

set -euo pipefail

. ./venv/bin/activate

echo mypy...
mypy . 

echo lint...
./lint.sh --disable=fixme,duplicate-code

echo pytest...
pytest --quiet
