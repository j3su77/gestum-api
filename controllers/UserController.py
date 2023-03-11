from config import SECRET_KEY, EXPIRE_TOKEN_TIME
from flask import abort, request, jsonify
from utils.db import db
from sqlalchemy.orm import joinedload

from models.User import User


import bcrypt

# Verifica si ya existe un usuario con el correo o documento
def check_user_exists(param_name, param_value, error_msg):
    user = User.query.filter_by(**{param_name: param_value}).first()
    if user:
        return jsonify({
            "msg": error_msg.format(param_value)
        }), 400
    return None


# ------------------- crear usuario ----------------------
def new_user():
    # Se obtiene los datos de la request
    try:
        correo = request.json['correo']
        contrasena = request.json['contrasena']
        nombre = request.json['nombre']
        apellidos = request.json['apellidos']
        telefono = request.json['telefono']
        tipo_documento = request.json['tipo_documento']
        documento = request.json['documento']
    except KeyError as e:
        response = jsonify(
            {'error': f"Falta el campo '{ e.args[0] }' en la solicitud"})
        response.status_code = 400
        return response

    # Verificando el correo
    response = check_user_exists(
        'correo', correo, 'Ya existe un usuario con el email: {}')
    if response:
        return response

    # Verificando el documento
    response = check_user_exists(
        'documento', documento, 'Ya existe un usuario con el documentos: {}')
    if response:
        return response

    # Se encripta la contraseña
    hashed_password = bcrypt.hashpw(
        contrasena.encode('utf-8'), bcrypt.gensalt())

    try:
        new_user = User(correo=correo, contrasena=hashed_password, nombre=nombre,
                        apellidos=apellidos, telefono=telefono, documento=documento, tipo_documento=tipo_documento)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "msg": f"Usuario: {nombre} {apellidos} fue registrado exitosamente!"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "msg": "Upps ocurrio un error, contacte al administrador del sistema",
            "error": str(e)
        }), 400


# ------------------- obtener usuarios ----------------------
def get_users():
    users = User.query.filter_by(activo=1).all()
    return jsonify([user.to_dict() for user in users])


# ------------------- obtener usuario ----------------------
def get_user(user_id):
    user = User.query.filter_by(id_usuario=user_id, activo=1).first()
    if not user:
        return jsonify({
            "msg": f"Usuario no registrado con ID: {user_id}"
        }), 400

    return jsonify(user.to_dict())


# ------------------- actualizar usuario ----------------------
def update_user(user_id):
    user = User.query.filter_by(id_usuario=user_id, activo=1).first()

    if not user:
        return jsonify({
            "msg": f"Usuario no registrado con ID: {user_id}"
        }), 400

    data = request.get_json()
    correo = data.get('correo')
    documento = data.get('documento')
    if correo and correo != user.correo:
        user_with_email = User.query.filter_by(correo=correo, activo=1).filter(User.id_usuario != user_id).first()
        if user_with_email:
            return jsonify({
                "msg": f"El correo {correo} ya está registrado"
            }), 400

    if documento and documento != user.documento:
        user_with_doc = User.query.filter_by(documento=documento, activo=1).filter(User.id_usuario != user_id).first()
        if user_with_doc:
            return jsonify({
                "msg": f"El correo {documento} ya está registrado"
            }), 400

    user.nombre = data.get('nombre', user.nombre)
    user.apellidos = data.get('apellidos', user.apellidos)
    user.correo = data.get('correo', user.correo)
    user.tipo_documento = data.get('tipo_documento', user.tipo_documento)
    user.documento = data.get('documento', user.documento)
    user.telefono = data.get('telefono', user.telefono)

    db.session.commit()

    return jsonify(user.to_dict())


# ------------------- cambiar contraseña ----------------------
def change_password(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "msg": f"Usuario no registrado con ID: {user_id}"
        }), 400

    current_password = request.json.get('actual_contrasena')
    new_password = request.json.get('nueva_contrasena')

    # notifica si la contraseña es válida
    passwordValid = bcrypt.checkpw(current_password.encode(
        'utf-8'), user.contrasena.encode('utf-8'))
    if not passwordValid or not user:
        return jsonify({'msg': 'la contrasena ingresada no coincide con la contrasena actual'}), 400

    # se encripta y guarda la nueva contraseña
    user.contrasena = bcrypt.hashpw(
        new_password.encode('utf-8'), bcrypt.gensalt())

    db.session.commit()

    return jsonify({'msg': 'Contraseña cambiada exitosamente'})
