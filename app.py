from flask import Flask, jsonify, request
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)

# Token authentication
auth = HTTPTokenAuth(scheme='Bearer')

# Mock data for users and tokens
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]

tokens = {
    "mysecrettoken": "john",
    "anothertoken": "jane"
}

# Authentication check
# Authorization: Bearer mysecrettoken


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]  # return the username associated with the token
    return None

# 1. Get all users (requires authentication)


@app.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    return jsonify(users)

# 2. Get user by ID (requires authentication)


@app.route('/users/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

# 3. Create a new user (requires authentication)


@app.route('/users', methods=['POST'])
@auth.login_required
def create_user():
    new_user = request.json
    new_user['id'] = len(users) + 1
    users.append(new_user)
    return jsonify(new_user), 201

# 4. Update user by ID (requires authentication)


@app.route('/users/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.update(request.json)
    return jsonify(user)

# 5. Delete user by ID (requires authentication)


@app.route('/users/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_user(id):
    user = next((u for u in users if u['id'] == id), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    users.remove(user)
    return jsonify({'message': 'User deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
