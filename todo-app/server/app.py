from flask import Flask
from flask_cors import CORS
from models import db, bcrypt
from routes import routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
bcrypt.init_app(app)
app.register_blueprint(routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
