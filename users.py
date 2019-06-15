from flask import *

from database import auth_db

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


@bp.route('/users/<username>/settings/')
def show_settings(username):
    if g.user is None or g.user['username'] != username:
        abort(403)
    return render_template('settings.html', userlist=list(auth_db.get_userlist()))


@bp.route('/users/<username>/settings/edit_description', methods=('POST',))
def edit_description(username):
    if g.user is None or g.user['username'] != username:
        abort(403)
    auth_db.set_user_description(username, request.form['description'])
    return '', 204


@bp.route('/users/<username>/settings/change_pw', methods=('POST',))
def change_pw(username):
    if g.user is None or g.user['username'] != username:
        abort(403)
    if request.form['password'] == '' or request.form['password'] != request.form['passwordAgain']:
        return 'wrongPassword', 403
    auth_db.set_user_password(g.user['username'], request.form['password'])
    return '', 204
