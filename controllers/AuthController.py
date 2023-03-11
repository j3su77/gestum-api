from config import SECRET_KEY, EXPIRE_TOKEN_TIME
from flask import request, jsonify
from utils.db import db
from sqlalchemy.orm import joinedload

from models.User import User
from models.Role import Role

import bcrypt
import jwt

from datetime import datetime, timedelta


# ------------------- Login ----------------------
def login():
    email = request.json['email']
    password = request.json['password']

    # user = User.query.filter_by(correo=email).first()

    # obtenemos el usuario con su respectivo rol
    user = db.session.query(User, Role.nombre).\
        join(Role, User.rol_id == Role.id_rol).\
        filter(User.correo == email).\
        options(joinedload(User.roles)).\
        first()

    # notifica si el correo es válido 
    if not user:
        return jsonify({'msg': 'Correo y/o contraseña incorrecta (e)'}), 400

    # notifica si la contraseña es válida
    passwordValid = bcrypt.checkpw(password.encode('utf-8'), user[0].contrasena.encode('utf-8'))
    if not passwordValid or not user:
        return jsonify({'msg': 'Correo y/o contraseña incorrecta (p)'}), 400

    # crea el tiempo de expiración del token
    expiration = datetime.utcnow() + timedelta(minutes=EXPIRE_TOKEN_TIME) 

    # role = Role.query.filter_by(id_rol=user.rol_id).first()

    # se crea el objeto con los datos relevantes para el token
    payload = {
        'email': email,
        'name': user[0].nombre,
        'lastName': user[0].apellidos,
        'role': str(user[1]),
        'exp': expiration
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
   
    return jsonify(token)


