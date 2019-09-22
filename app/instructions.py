from flask import Blueprint, send_file, url_for, redirect

BLUEPRINT = Blueprint("instructions", __name__)


@BLUEPRINT.route("/")
def default():
    return redirect(url_for(f"{BLUEPRINT.name}.{get_instructions.__qualname__}"))


@BLUEPRINT.route("/instructions")
def get_instructions():
    return send_file("../instructions.html")
