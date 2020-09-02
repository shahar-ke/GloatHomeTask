from flask import Blueprint

white_list = Blueprint('_users', __name__)
auth = HTTPBasicAuth()

@app_users.route('/api/v1/users/whitelist', methods=['GET'])
@auth.login_required
def get_resource():
    return jsonify({'username': user.username}), 201