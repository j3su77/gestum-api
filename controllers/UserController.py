from config import SECRET_KEY
from flask import request, jsonify

from models.User import User, db

import bcrypt
import jwt
import time

# ------------------- Sign Up ----------------------
def new_user():
    try:
        email = request.json['email']
        password = request.json['password']
        name = request.json['name']
        phone = request.json['phone']
    except KeyError as e:
        response = jsonify({'error': f"Falta el campo '{ e.args[0] }' en la solicitud"})
        response.status_code = 400
        return response 


    user = User.query.filter_by(correo=email).first()

    if user:
        return jsonify({
            "msg": f"Ya existe un usuario con el email {email}"
        }), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        new_user = User(correo=email, contrasena=hashed_password, nombre=name, telefono=phone, rol="cliente")
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "msg": f"Usuario {name} registrado exitosamente!"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "Upps ocurrio un error",
            "error": str(e)
        }), 400



# ------------------- Login ----------------------
def login():
    email = request.json['email']
    password = request.json['password']


    user = User.query.filter_by(correo=email).first()

    if not user:
        return jsonify({'msg': 'Correo y/o contraseña incorrecta (e)'}), 400

    passwordValid = bcrypt.checkpw(password.encode('utf-8'), user.contrasena.encode('utf-8'))
    if not passwordValid or not user:
        return jsonify({'msg': 'Correo y/o contraseña incorrecta (p)'}), 400


    payload = {
        'email': email,
        'name': user.nombre,
        'rol': user.rol,
        'timestamp': int(time.time())
    }
    print(SECRET_KEY)
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    return jsonify(token)


