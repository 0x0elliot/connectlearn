import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager
from flask_avatars import Avatars, _Avatars
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
BASEDIR = os.path.dirname(os.path.abspath(__file__))
avatars = Avatars()
_avatars = _Avatars()
mail = Mail()