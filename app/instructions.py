import markdown
from flask import render_template, Markup
from flask import url_for, redirect
from flask import Blueprint, current_app

bp = Blueprint("instructions", __name__,)


@bp.route('/')
def default():
    return redirect(url_for(f"{bp.name}.{get_instructions.__qualname__}"))


@bp.route('/instructions')
def get_instructions():
    instructionsFile = "README.md"
    current_app.logger.info(f'Serving {instructionsFile}')
    instructions = "".join(open(instructionsFile, 'r').readlines())
    body = Markup(markdown.markdown(
        instructions, extensions=markdown_extensions()))
    return render_template('index.html', content=body)


def markdown_extensions():
    return ['markdown.extensions.nl2br',
            'markdown.extensions.codehilite',
            'markdown.extensions.extra',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code',
            'markdown.extensions.footnotes']
