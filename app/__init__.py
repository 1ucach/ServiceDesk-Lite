from flask import Flask
from .database import init_db
from .routes.main_routes import main_bp
from .routes.client_routes import client_bp
from .routes.ticket_routes import ticket_bp


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["DATABASE"] = "servicedesk.db"

    init_db()

    app.register_blueprint(main_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(ticket_bp)

    return app
