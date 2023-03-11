from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy.orm import validates
from utils.db import db
from models.Role import Role

class TypeDoc(Enum):
    CC = 'CC'
    TI = 'TI'
    CE = 'CE'

class User(db.Model):
    __tablename__ = 'usuarios'
    id_usuario      = db.Column(db.Integer,    primary_key=True)
    nombre          = db.Column(db.String(50), nullable=False)
    apellidos       = db.Column(db.String(50), nullable=False)
    correo          = db.Column(db.String(50), unique=True, nullable=False)
    contrasena      = db.Column(db.String(50), nullable=False)
    tipo_documento  = db.Column(db.Enum(TypeDoc), default=TypeDoc.CC, nullable=False )
    documento       = db.Column(db.String(15), nullable=False, unique= True )
    telefono        = db.Column(db.String(15), nullable=False)
    rol_id          = db.Column(db.Integer, db.ForeignKey(Role.id_rol), default=3)
    activo          = db.Column(db.Integer, nullable=False, default=1)
    created_at      = db.Column(db.TIMESTAMP)

    roles = db.relationship('Role', backref='usuarios', lazy=True)

    def to_dict(self):
        tipo_documento = str(self.tipo_documento)
        tipo_documento_nombre = tipo_documento.split('.')[1] if tipo_documento.count('.') > 0 else tipo_documento
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'correo': self.correo,
            'tipo_documento': tipo_documento_nombre,
            'documento': self.documento,
            'telefono': self.telefono,
            'rol': self.roles.nombre,
            'activo': self.activo,
            'created_at': self.created_at.isoformat()
        }


    @validates('tipo_documento')
    def validate_tipo(self, key, value):
        if value not in [t.name for t in TypeDoc]:
            raise ValueError('Tipo inválido')
        return value


    def __repr__(self):
        return '<user %r>' % self.nombre