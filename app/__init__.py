from flask import Flask
from . import instructions


def create_app():
    app = Flask(__name__)

    app.register_blueprint(instructions.bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
