from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('../main.cfg')
db = SQLAlchemy(app)
