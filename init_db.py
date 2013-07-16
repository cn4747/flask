# -*- coding: utf-8 -*-

from models.user import User
from models.settings import Settings, Lang
from models import db
from libraries.security import sha1

db.drop_all()

db.create_all()

adm_login = 'npp'
adm_mail = 'anton.baranovka@gmail.com'
adm_pass = sha1('44862647')
admin = User(adm_login, adm_pass, adm_mail, '')

languages = [Lang('ru', 'НПП &laquo;НасосПромСервис&raquo;'),
             Lang('en', 'Research and Production Enterprise &laquo;NasosPromService&raquo; Ltd.')]
title = Settings('site_title', languages)

db.session.add(admin)
db.session.add(title)

db.session.commit()
