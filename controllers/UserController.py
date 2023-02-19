
from flask import request, jsonify


from models.User import User, db

from flask_sqlalchemy import SQLAlchemy
from config import SECRET_KEY


import bcrypt
import jwt
import time


def new_user():
    email = request.json['email']
    password = request.json['password']

    # Validamos si el usuario ya existe en la base de datos
    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "msg": f"Ya existe un usuario con el nombre {email}"
        }), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        # Guardamos el usuario en la base de datos
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "msg": f"Usuario {email} creado exitosamente!"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "Upps ocurrio un error",
            "error": str(e)
        }), 400




# @app.route('/api/user/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    # Validamos si el usuario existe en la base de datos
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'msg': f'No existe un usuario con el nombre {email} en la base de datos'}), 400

    # Validamos password
    passwordValid = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))
    if not passwordValid:
        return jsonify({'msg': 'Password incorrecta'}), 400

    # Generamos token
    payload = {
        'email': email,
        'timestamp': int(time.time())
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    return jsonify(token)


