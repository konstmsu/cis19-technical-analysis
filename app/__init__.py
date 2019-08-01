from flask import Flask
from . import instructions, evaluate


def create_app():
    app = Flask(__name__)

    app.register_blueprint(instructions.bp)
    app.register_blueprint(evaluate.bp)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
