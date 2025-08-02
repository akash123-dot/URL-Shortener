from flask import current_app
import jwt
import datetime


def generate_token(user_id):
    secret_key = current_app.config['SECRET_KEY']
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90)
         }
    
    return jwt.encode(payload, secret_key, algorithm='HS256')


def decode_token(token):
    secret_key = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None