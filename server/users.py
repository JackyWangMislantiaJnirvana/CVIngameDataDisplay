from flask import *

from server.auth import login_required
from server.database import auth_db

bp = Blueprint('users', __name__)


@bp.route('/users/')
def user_list():
    users = auth_db.get_userlist()
    return render_template('user_list.html', users=users)


@bp.route('/users/<username>/')
def user_page(username):
    return redirect(url_for('users.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard')
def show_dashboard(username):
    desc = auth_db.get_user(username)['description']
    datasets = {  # TODO: replace with real db queries
        "5c8d632f": {
            "name": "Generator",
            "data": [
                {
                    'type': 'text',
                    'key': 'Current generating',
                    'value': "50.0 EU/t"
                },
                {
                    'type': 'ratio',
                    'key': 'Storage',
                    'value_text': '70693/131072',
                    'value_ratio': '53.9%'
                }
            ]
        },
        "512a632f": {
            "name": "Thermal Generator",
            "data": [
                {
                    'type': 'text',
                    'key': 'Current generating',
                    'value': "128.0 EU/t"
                },
                {
                    'type': 'ratio',
                    'key': 'Storage',
                    'value_text': '18273/131072',
                    'value_ratio': '13.9%'
                }
            ]
        }
    }
    return render_template('dashboard.html', username=username, desc=desc, datasets=datasets)


@login_required
@bp.route('/settings/')
def show_settings():
    if g.user is None:
        abort(403)
    if auth_db.is_admin(g.user['username']):
        return render_template('settings.html', userlist=list(auth_db.get_userlist()),
                               invcode_list=list(auth_db.get_invcode_list()))
    else:
        return render_template('settings.html', userlist=[], invcode=[])


@bp.route('/settings/edit_description', methods=('POST',))
def edit_description():
    if g.user is None:
        abort(403)
    auth_db.set_user_description(g.user['username'], request.form['description'])
    return '', 204


@bp.route('/settings/change_pw', methods=('POST',))
def change_pw():
    if g.user is None:
        abort(403)
    if not auth_db.validate_login(g.user['username'], request.form['passwordOld']):
        return 'WRONG_OLD_PASSWORD', 403
    if request.form['passwordNew'] == '' or request.form['passwordNew'] != request.form['passwordNewAgain']:
        return 'PASSWORD_NO_MATCH', 403
    auth_db.set_user_password(g.user['username'], request.form['passwordNew'])
    return '', 204


# admin permission:

@bp.route('/site_management/')
def block_site_management():
    abort(404)


@bp.route('/site_management/set_admin', methods=('POST',))
def set_admin():
    if g.user is None or not auth_db.is_admin(g.user['username']):
        return "PERMISSION_DENIED", 403
    if auth_db.get_user(request.values['username']) is None:
        return "USER_NOT_FOUND", 404
    auth_db.set_admin(request.values['username'], not auth_db.is_admin(request.values['username']))
    return "", 204


@bp.route('/site_management/reset_password', methods=('POST',))
def reset_password():
    if g.user is None or not auth_db.is_admin(g.user['username']):
        return jsonify({"text": "PERMISSION_DENIED", "password": ""})
    if auth_db.get_user(request.values['username']) is None:
        return jsonify({"text": "USER_NOT_FOUND", "password": ""})
    pw = auth_db.generate_strong_password()
    auth_db.set_user_password(request.values['username'], pw)
    return jsonify({"text": "SUCCESS", "password": pw})


@bp.route('/site_management/remove_user', methods=('POST',))
def remove_user():
    if g.user is None or not auth_db.is_admin(g.user['username']):
        return "PERMISSION_DENIED", 403
    if auth_db.get_user(request.values['username']) is None:
        return "USER_NOT_FOUND", 404
    auth_db.remove_user(request.values['username'])
    return "", 204


@bp.route('/site_management/append_invite_code', methods=('POST',))
def append_invite_code():
    if g.user is None or not auth_db.is_admin(g.user['username']):
        return jsonify({"text": "PERMISSION_DENIED", "invcode": {}})
    cid, code = auth_db.append_invite_code()
    return jsonify({"text": "SUCCESS", "invcode": {'id': cid, 'code': code}})


@bp.route('/site_management/remove_invite_code', methods=('POST',))
def remove_invite_code():
    if g.user is None or not auth_db.is_admin(g.user['username']):
        return "PERMISSION_DENIED", 403
    if not auth_db.invite_code_exists(request.values['code']):
        return "CODE_NOT_FOUND", 404
    auth_db.remove_invite_code(request.values['code'])
    return "", 204
