from flask import Flask
from . import instructions, evaluate


def create_app():
    app = Flask(__name__)

    app.register_blueprint(instructions.BLUEPRINT)
    app.register_blueprint(evaluate.BLUEPRINT)

    return app
