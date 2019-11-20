from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    migrate = Migrate(app, db)

    login = LoginManager(app)
    login.login_view = 'main.login'

    #
    from app.main import bp as main_routes_bp
    app.register_blueprint(main_routes_bp)
    return app
    from app import routes, models
