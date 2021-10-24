from .views import node

from app.views.extensions import preprocessing, create_app


def create_main_app(app_config=None):
    if app_config is None:
        return None

    app = create_app(app_config)

    app.register_blueprint(node)
    preprocessing()

    return app

