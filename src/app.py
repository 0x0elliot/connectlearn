import os
from dotenv import load_dotenv
from flask import Flask
from src.extension import db, login_manager, avatars, mail, migrate
from src.blueprints.user.routes import user
from src.blueprints.contact.routes import contact
from src.blueprints.main.routes import main


def create_app():
    load_dotenv(".env")
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'secretdevkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    app.config['AVATARS_SAVE_PATH'] = os.path.join(BASEDIR  , 'avatars')
    avatars.init_app(app)
    #extensions(app)
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            pass
    
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    app.register_blueprint(user)
    app.register_blueprint(contact)
    app.register_blueprint(main)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug = True)
