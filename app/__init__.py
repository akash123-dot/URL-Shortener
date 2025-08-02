from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    migrate.init_app(app, db)

    from app import auth
    app.register_blueprint(auth.auth_bp, url_prefix='/authenticate')

    from app import utils
    app.register_blueprint(utils.app_bp, url_prefix='/app')


    return app