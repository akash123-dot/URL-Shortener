from flask import Blueprint,request,jsonify
from app.models import User
from app import db
from app.token_check import decode_token, generate_token

auth_bp = Blueprint('auth', __name__)


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def check_token(token):
        token = decode_token(token)
        # return token['user_id']
        return token

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/gettoken', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = authenticate(username, password)
    if user:
        token = generate_token(user.id)
        return {'token': token}, 200
    else:
        return {'message': 'Invalid username or password'}, 401
    
