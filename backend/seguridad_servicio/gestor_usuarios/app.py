from flask import Flask
from flask_cors import CORS
from gestor_usuarios.aplicacion.lecturas.ping import ping_bp
from gestor_usuarios.aplicacion.lecturas.home import home_bp
from gestor_usuarios.aplicacion.lecturas.login import login_user_bp
from gestor_usuarios.aplicacion.escrituras.registrar_user import registrar_user_bp
from gestor_usuarios.infraestructura.config import Config
from gestor_usuarios.infraestructura.database import init_db

URL_PREFIX = '/api/v1/seguridad/gestor_usuarios'
URL_SIGNUP = URL_PREFIX+'/w/signup'
URL_LOGIN = URL_PREFIX+'/r/auth/login'
URL_HOME = "/"

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(registrar_user_bp, url_prefix=URL_SIGNUP)
app.register_blueprint(login_user_bp, url_prefix=URL_LOGIN)

if __name__ == '__main__':
    init_db(app)
    app.run(debug=True, host="0.0.0.0", port=3011)