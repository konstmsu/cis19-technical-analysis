from flask import Flask
from . import instructions, evaluate, sample_solver


def create_app():
    app = Flask(__name__)

    app.register_blueprint(instructions.BLUEPRINT)
    app.register_blueprint(evaluate.BLUEPRINT)
    app.register_blueprint(sample_solver.BLUEPRINT)

    return app
