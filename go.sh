#!/usr/bin/env bash

set -euo pipefail

. ./venv/bin/activate

echo pytest...
pytest --quiet

echo mypy...
mypy . 

echo lint...
./lint.sh