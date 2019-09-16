import markdown
from flask import Blueprint, current_app
from flask import render_template, Markup
from flask import url_for, redirect

BLUEPRINT = Blueprint("instructions", __name__)


@BLUEPRINT.route("/")
def default():
    return redirect(url_for(f"{BLUEPRINT.name}.{get_instructions.__qualname__}"))


@BLUEPRINT.route("/instructions")
def get_instructions():
    instructions_file = "README.md"
    current_app.logger.info(f"Serving {instructions_file}")
    instructions = "".join(open(instructions_file, "r").readlines())
    body = Markup(markdown.markdown(instructions, extensions=markdown_extensions()))
    return render_template("index.html", content=body)


def markdown_extensions():
    return [
        "markdown.extensions.nl2br",
        "markdown.extensions.codehilite",
        "markdown.extensions.extra",
        "markdown.extensions.tables",
        "markdown.extensions.fenced_code",
        "markdown.extensions.footnotes",
    ]
