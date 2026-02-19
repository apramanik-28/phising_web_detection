# from flask import Flask
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from dotenv import load_dotenv
# import os

# from app.routes.auth_routes import auth_bp
# from app.routes.predict_routes import predict_bp
# from app.config.config import Config

# load_dotenv()

# def create_app():
#     app = Flask(__name__)

#     app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
#     app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

#     CORS(app)
#     JWTManager(app)

#     app.register_blueprint(auth_bp, url_prefix="/api/auth")
#     app.register_blueprint(predict_bp, url_prefix="/api")

#     return app


# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from app.routes.auth_routes import auth_bp
from app.routes.predict_routes import predict_bp
from app.config.config import Config

load_dotenv()

# ✅ Create JWT object globally (IMPORTANT)
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # ========================
    # Configuration
    # ========================
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

    # ========================
    # Initialize Extensions
    # ========================
    CORS(app)

    # ✅ Proper factory initialization
    jwt.init_app(app)

    print("✅ JWT Manager Initialized")

    # ========================
    # Register Blueprints
    # ========================
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(predict_bp, url_prefix="/api")

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

