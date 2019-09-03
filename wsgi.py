import logging
from app import create_app

# pylint: disable=invalid-name
application = create_app()

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)
