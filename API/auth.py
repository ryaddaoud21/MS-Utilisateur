from flask import Blueprint, jsonify, request, make_response
from API.models import db, User
import secrets
import pika
import json

auth_blueprint = Blueprint('auth', __name__)

# Token storage (simple in-memory storage for now)
valid_tokens = {}


def generate_token():
    return secrets.token_urlsafe(32)


# RabbitMQ connection
def publish_message(queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))
    connection.close()


def listen_for_auth_requests():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='auth_requests')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        token = data.get('token')
        response = {"authenticated": False}

        # Verify token
        user = next((u for u, t in valid_tokens.items() if t == token), None)
        if user:
            response = {"authenticated": True, "role": valid_tokens[user]['role']}

        publish_message('auth_responses', response)

    channel.basic_consume(queue='auth_requests', on_message_callback=callback, auto_ack=True)
    print('Waiting for authentication requests...')
    channel.start_consuming()


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"msg": "Username and password required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = generate_token()
        valid_tokens[data['username']] = {"token": token, "role": user.role}
        return jsonify({"token": token}), 200

    return jsonify({"msg": "Invalid credentials"}), 401




@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    token = request.headers.get('Authorization').split('Bearer ')[1]
    user = next((u for u, t in valid_tokens.items() if t["token"] == token), None)

    if user:
        del valid_tokens[user]
        return jsonify({"msg": "Successfully logged out"}), 200

    return make_response(jsonify({"error": "Unauthorized"}), 401)
