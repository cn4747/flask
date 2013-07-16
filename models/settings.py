from models import db

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), unique=True)
    
    lang = db.relationship('Lang', order_by='Lang.id', backref='Settings')#, lazy='dynamic')

    def __init__(self, key, lang):
        self.key = key
        self.lang = lang

    def __repr__(self):
        return '<Settings %r, %r>' % (self.key, self.lang)

class Lang(db.Model):
    __tablename__ = 'settings_lang'
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String(2))
    value = db.Column(db.Text())
    
    parent_id = db.Column(db.Integer, db.ForeignKey('settings.id'))
    setting = db.relationship('Settings', backref='Lang')

    def __init__(self, lang, value):
        self.lang = lang
        self.value = value

    def __repr__(self):
        return '<Lang %r, %r>' % (self.lang, self.value)
