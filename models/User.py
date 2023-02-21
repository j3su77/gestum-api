from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base


db = SQLAlchemy()
Base = declarative_base()


class RolUsuario(str, Enum):
    administrador = 'administrador'
    cliente = 'cliente'
    ejecutor = 'ejecutor'

class User(db.Model):
    __tablename__ = 'usuarios'
    id_usuario      = db.Column(db.Integer,    primary_key=True)
    nombre          = db.Column(db.String(50), nullable=False)
    correo          = db.Column(db.String(50), unique=True, nullable=False)
    contrasena      = db.Column(db.String(50), nullable=False)
    telefono        = db.Column(db.String(15), nullable=False)
    rol             = db.Column(db.String(50), unique=True, nullable=True)

    def __repr__(self):
        return '<user %r>' % self.nombre