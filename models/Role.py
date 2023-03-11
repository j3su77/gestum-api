from utils.db import db


class Role(db.Model):
    __tablename__   = 'roles'
    id_rol          = db.Column(db.Integer, primary_key=True)
    nombre          = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<user %r>' % self.nombre