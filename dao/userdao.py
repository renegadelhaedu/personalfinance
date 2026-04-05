from extensions import db, ph
from models import User

class UserDAO:
    def __init__(self):
        self.db = db
        self.model = User

    def create_user(self, username, email, password):
        #hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        hashed_pw = ph.hash(password)
        new_user = self.model(username=username, email=email, password=hashed_pw)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()