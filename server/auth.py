import functools
import re
import uuid

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, abort
)

from server.database import auth_db

bp = Blueprint('auth', __name__)


def valid_username(name):
    return re.match('^[0-9a-zA-Z_]{1,16}$', name) is not None


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    username = session.get("username")

    if username is None:
        g.user = None
    else:
        g.user = auth_db.get_user(username)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if auth_db.validate_login(username, password):
            session.clear()
            session['username'] = username
            return '', 204
        else:
            return abort(403)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if g.user is not None:
        return redirect('/')

    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        password = request.form['password']
        passwordAgain = request.form['passwordAgain']
        inviteCode = request.form['inviteCode']

        if auth_db.username_exists(username) or not valid_username(username):
            return 'wrongUsername', 403
        elif password != passwordAgain:
            return 'wrongPassword', 403
        elif not auth_db.invite_code_exists(inviteCode):
            return 'wrongInvCode', 403
        else:
            api_secret = str(uuid.uuid4())
            auth_db.create_user(username, password, inviteCode, api_secret)
            return '', 204
