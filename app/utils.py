from flask import Blueprint,request,redirect,jsonify
from app.models import URLEntries
from app import db
from app.short_url import generate_short_url
from app.auth import check_token

app_bp = Blueprint('app', __name__)

def main_url(long_url):
    existing_url = URLEntries.query.filter_by(long_url=long_url).first()
    if existing_url:
        return existing_url.short_url
    else:
        new_url = URLEntries(long_url=long_url)
        new_url.short_url = generate_short_url()
        db.session.add(new_url)
        db.session.commit()
        return new_url.short_url
    
@app_bp.route('/shorten', methods=['POST'])
def shorten():
    
    data = request.get_json()
    if data:
        token = request.headers.get('Authorization')
        if token:
            user_id = check_token(token)
            if user_id:
                url = data.get('url')
                if url:
                    if not url.startswith(('http://', 'https://')):
                        return {'message': 'Invalid URL'}, 400
                    
                    short_url = main_url(url)
                    return jsonify({'short_url': f"http://127.0.0.1:5000/app/{short_url}"}), 200
                else:
                    return {'message': 'URL is required'}, 400
            else:
                return {'message': 'Invalid token'}, 401
        else:
            return {'message': 'Token is required'}, 401
                
    else:
         return {'message': 'Data is required'}, 400



@app_bp.route('/<short_url>', methods=['GET'])
def redirect_url(short_url):
    url = URLEntries.query.filter_by(short_url=short_url).first()
    if url:
        url.increment_access_count()
        db.session.commit()
        return redirect(url.long_url, code=302)
    else:
        return {'message': 'URL not found'}, 404