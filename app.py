from flask import Flask
from interfaces.routes import register_routes
from infrastructure.db import db, migrate
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    from infrastructure.db import db, Book, Member
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

    db.init_app(app)
    migrate.init_app(app, db)

    register_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
