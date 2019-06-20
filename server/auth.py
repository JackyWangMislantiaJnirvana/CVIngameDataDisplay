import functools
import re
import uuid

from flask import (
    Blueprint, g, redirect, render_template, request, session, url_for, abort
)

import server.database
import server.database.auth

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
        g.user = server.database.auth.get_user(username)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect('/')

    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if server.database.auth.validate_login(username, password):
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
        password_again = request.form['passwordAgain']
        invite_code = request.form['inviteCode']

        if server.database.auth.username_exists(username) or not valid_username(username):
            return 'wrongUsername', 403
        elif password != password_again:
            return 'wrongPassword', 403
        elif not server.database.auth.invite_code_exists(invite_code):
            return 'wrongInvCode', 403
        else:
            api_secret = str(uuid.uuid4())
            server.database.auth.create_user(username, password, invite_code, api_secret)
            return '', 204
