from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow

# Extensiones
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
ma = Marshmallow()

def create_app(config_name=None):
    load_dotenv(override=True)
    app = Flask(__name__)

    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Config')
        
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    # Importar modelos AQUÍ (IMPORTANTE para Flask-Migrate)
    from app.models import (
        User, Role, UserRole,
        Parking, ParkingZone, Cell,
        Vehicle, Registration,
        Invoice, Payment
    )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"Token inválido: {error}")
        return jsonify({"msg": "Token inválido"}), 422

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        print(f"Token no autorizado: {error}")
        return jsonify({"msg": "No autorizado"}), 401

    CORS(app, resources={r"/api/": {"origins": ""}}, supports_credentials=True)

    from app.routes.users import users_bp
    from app.routes.health import health_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(health_bp)

    return app