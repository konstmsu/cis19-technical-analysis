#!/usr/bin/env bash
python3 -m venv env
. ./env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt