import os
from flask import Flask

from app import instructions, evaluate, sample_solver
from app.sample_solver import ENABLE_SOLVER_KEY


def create_app():
    app = Flask(__name__)

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
