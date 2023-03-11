from flask import Blueprint

from controllers.AuthController import login

auth_bp = Blueprint('auth_bp', __name__)


auth_bp.route('/', methods=['POST'])(login)


# user_bp.route('/<int:user_id>', methods=['GET'])(show)
# user_bp.route('/<int:user_id>/edit', methods=['POST'])(update)
# user_bp.route('/<int:user_id>', methods=['DELETE'])(destroy)