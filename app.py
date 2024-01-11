# app.py
from flask import Flask, jsonify, request, make_response
from database_structure import User, License, app, db
import json
import jwt
from datetime import datetime, timedelta
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check if a token was sent
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token not included!'}, 401)
        # If we have a token, validate access by consulting bd.
        try:
            result = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            author = User.query.filter_by(id_author=result['id_author']).first()
        except:
            return jsonify({'message': 'Token is invalid'}, 401)
        return f(*args, **kwargs)
    return decorated

@app.route("/")
@token_required
def get_all_keys():
    licenses = License.query.all()
    license_list = []

    for license in licenses:
        data = {}
        data['license'] = license.license
        license_list.append(data)

    return jsonify({'Licenses': license_list})

@app.route("/keys/<string:key>", methods=['GET'])
def validate_key(key):
    license = License.query.filter_by(license=key).first()
    if license:
        return jsonify({'access': True})
    return jsonify({'access': False})

# Add a new key
@app.route("/keys", methods=['POST'])
@token_required
def add_access_key():
    data = request.get_json()

    new_license = License(license=data['license'])
    db.session.add(new_license)
    db.session.commit()

    return jsonify({'message': 'New license registered successfully!'})

# Delete an existing key
@app.route('/keys/<string:key>', methods=['DELETE'])
@token_required
def delete_license(key):
    try:
        license = License.query.filter_by(license=key).first()
        if license:
            db.session.delete(license)
            db.session.commit()
        return jsonify({'message': 'Key deleted successfully'})
    except Exception as error:
        print(error)
        return jsonify(f'Could not delete the key {key}')

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Invalid login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    user = User.query.filter_by(name=auth.username).first()
    if not user:
        return make_response('Invalid login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})
    if auth.password == user.password:
        token = jwt.encode({'id_author': user.id_author, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Invalid login', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0', debug=False)
