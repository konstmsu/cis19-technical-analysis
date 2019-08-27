#!/usr/bin/env bash
python -m venv env
. ./env/Scripts/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt