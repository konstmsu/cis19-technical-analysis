import logging

import markdown
from flask import render_template, Markup
from flask import url_for, redirect
from flask import Blueprint

logger = logging.getLogger(__name__)
bp = Blueprint("auth", __name__,)


@bp.route('/')
def default():
    return redirect(url_for('get_instructions'))


@bp.route('/instructions')
def get_instructions():
    logger.info("Received request for Instructions")
    instructions = "".join(open("README.md", 'r').readlines())
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
