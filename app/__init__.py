import os
from logging.config import dictConfig
import logging
from flask import Flask

from app import instructions, evaluate, sample_solver
from app.sample_solver import ENABLE_SOLVER_KEY


def create_app():
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {"format": "%(levelname)s in %(module)s: %(message)s"}
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": "INFO", "handlers": ["wsgi"]},
        }
    )
    logging.debug("logging.debug")
    logging.info("logging.info")
    logging.warning("logging.info")

    app = Flask(__name__)

    app.logger.debug("app.logger.debug")  # pylint: disable=no-member
    app.logger.info("app.logger.info")  # pylint: disable=no-member
    app.logger.warning("app.logger.warning")  # pylint: disable=no-member

    app.register_blueprint(instructions.BLUEPRINT)
    app.register_blueprint(evaluate.BLUEPRINT)
    app.register_blueprint(sample_solver.BLUEPRINT)

    app.config[ENABLE_SOLVER_KEY] = coerce_to_bool(
        os.environ.get(ENABLE_SOLVER_KEY), False
    )

    return app


def coerce_to_bool(value, default):
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        normalized = value.lower()
        if normalized in ["true"]:
            return True
        if normalized in ["false"]:
            return False

    if value in [None, ""]:
        return default

    raise Exception(f"Can't coerce {value} of type {type(value)} to bool")
