from app.exceptions.handlers import register_exception_handlers
from flask import Flask
import logging
from app.services.logging.logging_middleware import LoggingMiddleware
from app.core.extensions import db, cache, ma
from app.orm.schemas.base import ma
from app.core.settings import settings



def create_app():
    app = Flask(__name__)
    app.config.from_object(settings.get_env_config())
    register_extensions(app)
    register_views(app)
    register_commands(app)
    register_exception_handlers(app)
    configure_logger(app)
    
    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    
    if settings.debug:
        with app.app_context():
            cache.clear()

        with app.app_context():
            import app.orm.models

            db.drop_all()
            db.create_all()


def register_views(app):
    from app.api.views.goods import goods_page
    app.register_blueprint(goods_page)


def register_commands(app):
    from app.command.load_fixtures import fixtures
    app.register_blueprint(fixtures)


def configure_logger(app):
    """Configure loggers."""
    # app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    loggers = ["gunicorn.error", "app.sqltime"]
    for logger in loggers:
        app.logger.handlers.extend(logging.getLogger(logger).handlers)
