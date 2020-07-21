from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from resources.error import errors

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_pyfile('config.py')
    api = Api(app, errors=errors)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    from resources.routes import init_routes
    migrate = Migrate(app, db)
    init_routes(api)

    return app
