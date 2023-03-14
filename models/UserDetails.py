from utils.db import db
from models.User import User
from enum import Enum



class Type(Enum):
    direccion = 'direccion'
    especialidad = 'especialidad'

class UserDetails(db.Model):
    __tablename__   = 'usuario_detalles'
    id_detalle      = db.Column(db.Integer, primary_key=True)
    usuario_id      = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    tipo            = db.Column(db.Enum(Type), default=Type.direccion, nullable=False )
    detalle         = db.Column(db.String(100), nullable=False)

    usuario = db.relationship('User', backref='usuario_detalles', lazy=True)


    def __repr__(self):
        return '<userdatails %r>' % self.tipo