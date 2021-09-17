import os
from dotenv import load_dotenv
from flask import Flask
from src.extension import db, login_manager, avatars, mail, migrate
from src.blueprints.user.routes import user
from src.blueprints.contact.routes import contact
from src.blueprints.main.routes import main
import secrets

def extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    return None

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = secrets.token_hex(42)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    app.config['AVATARS_SAVE_PATH'] = os.path.join(BASEDIR  , 'avatars')
    avatars.init_app(app)
    extensions(app)

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    app.register_blueprint(user)
    app.register_blueprint(contact)
    app.register_blueprint(main)
    mail.init_app(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug = True)
