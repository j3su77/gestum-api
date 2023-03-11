from flask import Blueprint

from controllers.UserController import new_user, get_users, get_user, update_user, change_password

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/create', methods=['POST'])(new_user)
user_bp.route('/', methods=['GET'])(get_users)
user_bp.route('/<int:user_id>', methods=['GET'])(get_user)
user_bp.route('/<int:user_id>', methods=['PUT'])(update_user)
user_bp.route('/<int:user_id>/change-password', methods=['PUT'])(change_password)


# user_bp.route('/<int:user_id>', methods=['GET'])(show)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)