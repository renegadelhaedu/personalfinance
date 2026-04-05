from argon2 import PasswordHasher

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

ph = PasswordHasher()
db = SQLAlchemy()
#bcrypt = Bcrypt()
login_manager = LoginManager()