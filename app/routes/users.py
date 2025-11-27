from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.schemas import UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

users_bp = Blueprint('users', __name__, url_prefix='/api/users')
user_schema = UserSchema()

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = user_schema.load(data)
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # CAMBIO: username → email
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'msg': 'Credenciales incorrectas'}), 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/get', methods=['GET'])
@jwt_required()
def list_users():
    users = User.query.all()
    return jsonify(UserSchema(many=True).dump(users)), 200