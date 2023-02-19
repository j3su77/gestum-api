from flask import Blueprint

from controllers.UserController import new_user, login

user_bp = Blueprint('user_bp', __name__)

user_bp.route('/', methods=['POST'])(new_user)
user_bp.route('/login', methods=['POST'])(login)


# user_bp.route('/<int:user_id>', methods=['GET'])(show)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)