from flask import Flask
from .config.config import Config
from .extensions import mongo, bcrypt, cors, jwt   # 🔥 IMPORT jwt
from .routes.auth_routes import auth_bp
from .routes.predict_routes import predict_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    mongo.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)   # 🔥 THIS WAS MISSING

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(predict_bp, url_prefix="/api")
    return app
