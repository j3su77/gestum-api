
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from utils.db import db
from routes.auth_bp import auth_bp
from routes.user_bp import user_bp

app = Flask(__name__)


app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
cors = CORS(app)



cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})



# Importar rutas
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')


def pagina_no_encontrada(error):
    return jsonify({
            "msg": "Error"
        }), 201

if __name__ == '__main__':
    app.register_error_handler(404 , pagina_no_encontrada)
    app.run(debug=True)