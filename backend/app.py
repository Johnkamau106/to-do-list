import os
from flask import Flask
from flask_cors import CORS
from extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from models import User, Todo  # Import models
        from routes.auth import auth_bp
        from routes.todos import todos_bp

        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(todos_bp, url_prefix='/api')

        # Create the database if it doesn't exist
        if not os.path.exists(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')):
            db.create_all()

        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)