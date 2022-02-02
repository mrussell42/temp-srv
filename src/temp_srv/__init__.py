from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment

# Globally accessible libraries
db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, 
                instance_relative_config=False,
                template_folder='templates')
    app.config.from_object('config.Config')
    assets = Environment(app)
    assets.config['less_bin'] = '/usr/local/lib/node_modules/less/bin/lessc'
    assets.init_app(app)
    
    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes
        from .assets import compile_static_assets
        db.create_all()
        # Import Dash application
        from .plotlydash.dashboard import init_dashboard
        app = init_dashboard(app)

        compile_static_assets(assets)

        return app