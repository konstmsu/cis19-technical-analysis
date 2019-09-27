from flask import Blueprint, send_file, url_for, redirect, make_response, request

BLUEPRINT = Blueprint("instructions", __name__)

MATHS_SCALE_COOKIE = "mjx.menu"


@BLUEPRINT.route("/")
def default():
    return redirect(url_for(f"{BLUEPRINT.name}.{get_instructions.__qualname__}"), code=307)


@BLUEPRINT.route("/instructions")
def get_instructions():
    response = make_response(send_file("../instructions.html"))
    if MATHS_SCALE_COOKIE not in request.cookies:
        response.set_cookie(MATHS_SCALE_COOKIE, "scale%3A150")
    return response


@BLUEPRINT.route("/custom.css")
def get_custom_css():
    return send_file("../custom.css")


@BLUEPRINT.route("/favicon.ico")
def get_favicon():
    return send_file("../favicon.ico")


@BLUEPRINT.route("/static/sample_data.zip")
def get_sample_data():
    return send_file("../static/sample_data.zip", as_attachment=True)
