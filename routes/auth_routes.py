from flask import Blueprint, request, jsonify
from models import db, User
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing data'}), 400
    
    user = User(
        username=data['username'],
        role=data['role']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login')
@auth.login_required
def login():
    return jsonify({'message': 'Logged in successfully', 'user': auth.current_user().username}), 200
