from flask import Blueprint, request, jsonify, url_for, g
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import abort

from server_lib.models.database import db
from server_lib.models.user_model import User

app_users = Blueprint('app_users', __name__)

auth = HTTPBasicAuth()


@app_users.route('/api/v1/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('app_users.get_user', id=user.id, _external=True)})


@app_users.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username})

@auth.verify_password
def verify_passwordverify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app_users.route('/api/v1/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app_users.route('/api/v1/resource', methods=['GET'])
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.username})


@app_users.route('/api/v1/users/whitelist', methods=['POST'])
@auth.login_required
def post_whitelist():
    return jsonify({'data': 'Hello, %s, thanks for the whitelist!' % g.user.username}), 201
