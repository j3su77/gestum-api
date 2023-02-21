
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

from models.User import db
from routes.user_bp import user_bp

app = Flask(__name__)



app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
cors = CORS(app)



cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})



# Importar rutas
app.register_blueprint(user_bp, url_prefix='/api/user')



if __name__ == '__main__':
    app.run(debug=True)