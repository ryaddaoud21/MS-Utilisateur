from flask import Blueprint, jsonify, request, make_response
from API.models import User, db
import secrets
from functools import wraps

auth_blueprint = Blueprint('auth', __name__)

# Simulated token storage (for simplicity)
valid_tokens = {}


def generate_token():
    return secrets.token_urlsafe(32)


# Decorator to require a valid token
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        received_token = token.split('Bearer ')[1]
        user = next((u for u, t in valid_tokens.items() if t["token"] == received_token), None)

        if not user:
            return make_response(jsonify({"error": "Unauthorized"}), 401)

        request.user = user
        request.role = valid_tokens[user]['role']

        return f(*args, **kwargs)

    return decorated_function


# Login Endpoint
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not 'username' in data or not 'password' in data:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        token = generate_token()
        valid_tokens[user.username] = {"token": token, "role": user.role}
        return jsonify({"token": token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401



# Logout Endpoint
@auth_blueprint.route('/logout', methods=['POST'])
@token_required
def logout():
    token = request.headers.get('Authorization').split('Bearer ')[1]
    user = next((u for u, t in valid_tokens.items() if t["token"] == token), None)

    if user:
        del valid_tokens[user]
        return jsonify({"msg": "Successfully logged out"}), 200

    return make_response(jsonify({"error": "Unauthorized"}), 401)