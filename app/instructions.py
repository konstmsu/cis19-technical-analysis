from flask import Blueprint, send_file, url_for, redirect

BLUEPRINT = Blueprint("instructions", __name__)


@BLUEPRINT.route("/")
def default():
    return redirect(url_for(f"{BLUEPRINT.name}.{get_instructions.__qualname__}"))


@BLUEPRINT.route("/instructions")
def get_instructions():
    return send_file("../instructions.html")


@BLUEPRINT.route("/technical_analysis_sample_data.zip")
def get_sample_data():
    return send_file(
        "../sample_data/sample_data.zip",
        as_attachment=True,
        attachment_filename="technical_analysis_sample_data.zip",
    )
