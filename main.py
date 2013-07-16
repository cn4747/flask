# -*- coding: utf-8 -*-

from flask import Flask
from blueprints.admin import admin
from flaskext.babel import Babel
from flaskext.babel import Locale
from flask import g, request, session

app = Flask(__name__)
app.config.from_pyfile('main.cfg')
app.register_blueprint(admin, url_prefix='/adm')
babel = Babel(app)

@babel.localeselector
def get_locale():
    if 'lang' in session and session['lang'] != None:
        return session['lang']
    else:
        session['lang'] = request.accept_languages.best_match(['ru', 'en'])
        return session['lang']

if __name__ == '__main__':
    app.run(debug=True)
