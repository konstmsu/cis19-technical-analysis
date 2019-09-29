#! /usr/bin/env bash

FLASK_ENV=development ENABLE_SOLVER=true flask run
# ENABLE_SOLVER=true gunicorn wsgi --threads 3
# ENABLE_SOLVER=true heroku local web=3