
from flask import Flask
from flask_migrate import Migrate

from models.User import db

from routes.user_bp import user_bp

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL

app.config.from_object('config')

db.init_app(app)
migrate = Migrate(app, db)

# Importar rutas


app.register_blueprint(user_bp, url_prefix='/api/user')




if __name__ == '__main__':
    app.run(debug=True)