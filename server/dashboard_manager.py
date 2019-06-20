from flask import *

from server.database import auth, dashboard

bp = Blueprint('dashboard_manager', __name__)


@bp.route('/users/<username>/dashboard')
def show_dashboard(username):
    desc = auth.get_user(username)['description']
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


@bp.route('/users/<username>/update', methods=('POST',))
def update(username):
    print(request.form)
    return redirect(url_for('users.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard/add', methods=('POST',))
def add(username):
    print(request.form)
    if username != g.user['username']:
        abort(403)
    return redirect(url_for('users.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard/remove', methods=('POST',))
def remove(username):
    print(request.form)
    if username != g.user['username']:
        abort(403)
    return redirect(url_for('users.show_dashboard', username=username))
