from flask import Blueprint, render_template
from flask import g, request, redirect, session, url_for
from jinja2 import TemplateNotFound
from models.user import User
from models.settings import Settings, Lang
from models import db
from libraries.security import sha1
from flask.ext.babel import gettext
_ = gettext

from functools import wraps

import logging

logging.basicConfig(filename='db.log')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

admin = Blueprint('admin', __name__)

"""A decorator function for checking user authentication
Shows login form if user is not logged in or has an expired session
"""
def auth(fn):
    """Check if user is authorized
    """
    def is_authorized():
        # If session hash is set
        if 'hash' in session:
            # Check hash value in db and get user data if found
            user = db.session.query(User).filter_by(
                        session=session['hash']).first()
            # If user hash is in db, allow function execution
            if user is not None:
                return True
        
        return False
    
    """Set error message and render template with login form
    """
    def request_auth():
        expired = _('Your session has expired. Please log in again')
        return render_template('admin/login.html', message=expired)
    
    @wraps(fn)
    def login_required(*args, **kwargs):
        if is_authorized():
            return fn(*args, **kwargs)
        
        return request_auth()
    
    return login_required

@admin.route('/', methods=['GET', 'POST'])
def index():
    # If user just gets to a page
    if request.method == 'GET':
        # If user is logged and has a session cookie, go to panel
        if 'hash' in session:
            user = db.session.query(User).filter_by(
                        session=session['hash']).first()
            if user is None:
                return render_template('admin/login.html')
            else:
                return redirect(url_for('admin.panel'))
        # If not, ask to log in
        else:
            return render_template('admin/login.html')
    # If user submitted a form with login and password
    else:
        # Get user data
        user = db.session.query(User).filter_by(
                    login=request.form['login'],
                    password=sha1(request.form['password'])
                    ).first()
        # If no such user, display a message and ask to relogin
        if user is None:
            return render_template('admin/login.html',
                        message=_('Wrong username or password!'),
                        global_language=session['lang'])
        # Otherwise, go to panel
        else:
            # Generate a SHA1 hash for user and update in db
            session['hash'] = sha1(user.login + user.email)
            user.session = session['hash']
            db.session.commit();
            
            return redirect(url_for('admin.panel'))

@admin.route('/panel')
@auth
def panel():
    return render_template('admin/panel.html',
                            global_language=session['lang'])

@admin.route('/settings', methods=['GET', 'POST'])
@admin.route('/settings/<action>', methods=['GET', 'POST'])
@auth
def settings(action=None):
    data = dict()
    # Select values language from session by default
    if action == None or action == 'None':
        lang = session['lang']
    # Or set language manually
    else:
        lang = action

    if request.method == 'POST':
        # Used reversed() to keep proper order
        for index, item in reversed(request.form.items()):
            # Check field to be like s[]
            if index[0:2] == 's[':
                # Cut the key from array s[some_key]
                key = index[2:-1]
                # Get parameter from database
                get_param = db.session.query(Settings).select_from(db.join(Settings, Lang)).filter(Lang.lang==lang, Settings.key==key).first()
                print get_param
                # If no such parameter, create it and insert
                if get_param is None:
                    get_param = Settings(key, [Lang(lang, item)])
                # Otherwise update
                else:
                    get_param.lang[0].lang = lang
                    get_param.lang[0].value = item
                db.session.add(get_param)
            db.session.commit()

    settings = db.session.query(Settings.key, Lang.value).join(Settings.lang).filter(Lang.lang==lang)
    for index, item in enumerate(settings):
        data[item.key] = item.value

    return render_template('admin/settings.html',
                            settings=data,
                            language=lang,
                            global_language=session['lang'])

@admin.route('/user', methods=['GET', 'POST'])
@auth
def user():
    error = None
    msg = ''
    msg_empty_fields = _('No empty fields allowed (excl. password)')
    msg_success = _('Data updated')
    
    user = db.session.query(User).filter_by(
                    session=session['hash']).first()
    
    if request.method == 'POST':
        # If any of passwords is empty, do not consider them
        if request.form['pass1'] == '' and request.form['pass2'] == '':
            # Check updating fields to be filled
            if '' in [request.form['login'], request.form['email']]:
                msg = msg_empty_fields
                error = True
            else:
                user.login = request.form['login']
                user.email = request.form['email']
                db.session.commit()
                msg = msg_success
        # If passwords not matching
        elif request.form['pass1'] != request.form['pass2']:
            msg = _('Passwords should match')
            error = True
        else:
            # Check the form to be filled
            empty = None
            for value in request.form:
                if request.form[value] == '':
                    print '%r => %r' % (value, request.form[value])
                    empty = True
            # If not, assign error
            if empty is True:
                msg = msg_empty_fields
                error = True
            # Otherwise update
            else:
                user.login = request.form['login']
                user.password = sha1(request.form['pass1'])
                user.email = request.form['email']
                db.session.commit()
                msg = msg_success
    
    form = { 'login' : user.login, 'email' : user.email }

    return render_template('admin/user.html', 
                form=form, 
                error=error, 
                msg=msg,
                global_language=session['lang'])

@admin.route('/lang/<language>')
@auth
def lang(language=None):
    session['lang'] = language
    return redirect(request.referrer)

@admin.route('/logout')
def logout():
    if 'hash' in session:
        user = db.session.query(User).filter_by(
                    session=session['hash']).first()
        user.session = ''
        session.clear()
    
    return render_template('admin/login.html',
                message=_('You logged out'))
