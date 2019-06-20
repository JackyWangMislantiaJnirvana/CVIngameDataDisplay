from flask import *

from server.auth import login_required
from server.database import auth

bp = Blueprint('users', __name__)


@bp.route('/users/')
def user_list():
    users = auth.get_userlist()
    return render_template('user_list.html', users=users)


@bp.route('/users/<username>/')
def user_page(username):
    return redirect(url_for('dashboard_manager.show_dashboard', username=username))


@login_required
@bp.route('/settings/')
def show_settings():
    if g.user is None:
        abort(403)
    if auth.is_admin(g.user['username']):
        return render_template('settings.html', userlist=list(auth.get_userlist()),
                               invcode_list=list(auth.get_invcode_list()))
    else:
        return render_template('settings.html', userlist=[], invcode=[])


@bp.route('/settings/edit_description', methods=('POST',))
def edit_description():
    if g.user is None:
        abort(403)
    auth.set_user_description(g.user['username'], request.form['description'])
    return '', 204


@bp.route('/settings/change_pw', methods=('POST',))
def change_pw():
    if g.user is None:
        abort(403)
    if not auth.validate_login(g.user['username'], request.form['passwordOld']):
        return 'WRONG_OLD_PASSWORD', 403
    if request.form['passwordNew'] == '' or request.form['passwordNew'] != request.form['passwordNewAgain']:
        return 'PASSWORD_NO_MATCH', 403
    auth.set_user_password(g.user['username'], request.form['passwordNew'])
    return '', 204


# admin permission:

@bp.route('/site_management/')
def block_site_management():
    abort(404)


@bp.route('/site_management/set_admin', methods=('POST',))
def set_admin():
    if g.user is None or not auth.is_admin(g.user['username']):
        return "PERMISSION_DENIED", 403
    if auth.get_user(request.values['username']) is None:
        return "USER_NOT_FOUND", 404
    auth.set_admin(request.values['username'], not auth.is_admin(request.values['username']))
    return "", 204


@bp.route('/site_management/reset_password', methods=('POST',))
def reset_password():
    if g.user is None or not auth.is_admin(g.user['username']):
        return jsonify({"text": "PERMISSION_DENIED", "password": ""})
    if auth.get_user(request.values['username']) is None:
        return jsonify({"text": "USER_NOT_FOUND", "password": ""})
    pw = auth.generate_strong_password()
    auth.set_user_password(request.values['username'], pw)
    return jsonify({"text": "SUCCESS", "password": pw})


@bp.route('/site_management/remove_user', methods=('POST',))
def remove_user():
    if g.user is None or not auth.is_admin(g.user['username']):
        return "PERMISSION_DENIED", 403
    if auth.get_user(request.values['username']) is None:
        return "USER_NOT_FOUND", 404
    auth.remove_user(request.values['username'])
    return "", 204


@bp.route('/site_management/append_invite_code', methods=('POST',))
def append_invite_code():
    if g.user is None or not auth.is_admin(g.user['username']):
        return jsonify({"text": "PERMISSION_DENIED", "invcode": {}})
    cid, code = auth.append_invite_code()
    return jsonify({"text": "SUCCESS", "invcode": {'id': cid, 'code': code}})


@bp.route('/site_management/remove_invite_code', methods=('POST',))
def remove_invite_code():
    if g.user is None or not auth.is_admin(g.user['username']):
        return "PERMISSION_DENIED", 403
    if not auth.invite_code_exists(request.values['code']):
        return "CODE_NOT_FOUND", 404
    auth.remove_invite_code(request.values['code'])
    return "", 204
