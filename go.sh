#!/usr/bin/env bash

set -euo pipefail

. ./venv/bin/activate

echo instructions.html
jupyter nbconvert --no-input instructions.ipynb

echo mypy...
mypy . 

echo lint...
./lint.sh --disable=fixme,duplicate-code

echo pytest...
pytest --quiet
