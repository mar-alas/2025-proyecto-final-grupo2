from flask import Flask
from seedwork_compartido.aplicacion.lectura.ping import ping_bp
from aplicacion.lecturas.home import home_bp
from aplicacion.escrituras.registrar_user import registrar_user_bp

URL_PREFIX = '/api/v1/seguridad/gestor_usuarios'
URL_SIGNUP = URL_PREFIX+'/signup'
URL_HOME = "/"

app = Flask(__name__)
app.register_blueprint(ping_bp, url_prefix=URL_PREFIX)
app.register_blueprint(home_bp, url_prefix=URL_HOME)
app.register_blueprint(registrar_user_bp, url_prefix=URL_SIGNUP)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3011)