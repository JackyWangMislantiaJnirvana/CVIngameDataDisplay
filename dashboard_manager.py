from flask import *

bp = Blueprint('dashboard_manager', __name__)


@bp.route('/users/<username>/update', methods=('POST',))
def update(username):
    print(request.form)
    return redirect(url_for('users.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard/add', methods=('POST',))
def add(username):  # 权限判断！！！
    print(request.form)
    if username != g.user['username']:
        abort(403)
    return redirect(url_for('users.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard/remove', methods=('POST',))
def remove(username):  # 权限判断！！！
    print(request.form)
    return redirect(url_for('users.show_dashboard', username=username))
