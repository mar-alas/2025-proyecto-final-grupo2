from aplicacion import create_app
from infraestructura.database import init_db
from flask_cors import CORS

app = create_app()
CORS(app)

if __name__ == '__main__': # pragma: no cover
    init_db(app)
    app.run(debug=True, host="0.0.0.0", port=3001)