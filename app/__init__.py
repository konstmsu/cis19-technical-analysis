import os

from flask import Flask
from app import instructions


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.register_blueprint(instructions.bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
