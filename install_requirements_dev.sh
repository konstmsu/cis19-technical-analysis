#!/usr/bin/env bash

set -euo pipefail

python3.7 -m venv venv
. ./venv/bin/activate
python --version
pip install -r requirements.txt
pip install -r requirements-dev.txt