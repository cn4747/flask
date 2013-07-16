from models import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String(100), unique=True)
    session = db.Column(db.String(40))

    def __init__(self, login, password, email, session):
        self.login = login
        self.password = password
        self.email = email
        self.session = session

    def __repr__(self):
        return '<User %r>' % self.login
