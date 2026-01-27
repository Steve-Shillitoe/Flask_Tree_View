from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create extension instances.
# These are initialised with the Flask application in create_app().
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
    Create and configure the Flask application.

    This function implements the application factory pattern. It creates
    the Flask application instance, loads configuration, initialises
    extensions, registers Blueprints, and returns the configured app.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Create the Flask application instance
    app = Flask(__name__)

    # Load application configuration (e.g. database connection settings)
    app.config.from_object("config")

    # Initialise extensions with the application
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models so SQLAlchemy can discover them
    # This must occur after extensions are initialised
    from AnimalKingdom import models  # noqa: F401

    # Register Blueprints that define routes and views
    from AnimalKingdom.routes import bp
    app.register_blueprint(bp)

    return app
