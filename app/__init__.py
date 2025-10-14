def create_app(config_overrides=None):
    """Create and configure the Flask app with Flask-RESTX for Swagger UI."""
    from flask import Flask
    from flask_restx import Api
    from .database import db
    from .routes import api as products_api

    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI="sqlite:///streamoid.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    # Setup Flask-RESTX API
    api = Api(app, title="Streamoid Product Service", version="1.0", doc="/docs")
    api.add_namespace(products_api, path="/")

    return app
