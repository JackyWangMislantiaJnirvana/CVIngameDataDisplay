import logging
import json

from flask import Blueprint, request, render_template, abort, redirect, url_for, g

from server import utils
from server import database
from server.database.dashboard.dataset_delegate import DatasetDelegate
from server.database import auth
from server.database.dashboard import dashboard_db

bp = Blueprint('dashboard_manager', __name__)


@bp.route('/users/<username>/dashboard/do_render.cgi', methods=('GET',))
def do_render(username):
    target = request.args['dataset']  # target is the 8-digit hash for the dataset
    delegate = DatasetDelegate(username, int(target, 16))
    return delegate.render(bool(request.args['is_modal']))


@bp.route('/users/<username>/dashboard/query_last_update.cgi')
def query_last_update(username):
    target = request.args['dataset']  # target is the 8-digit hash for the dataset
    delegate = DatasetDelegate(username, int(target, 16))
    return str(delegate.last_update)


@bp.route('/users/<username>/dashboard/')
def show_dashboard(username):
    desc = auth.get_user(username)['description']
    datasets = [{'id': utils.to_dataset_hash(x['id']), 'title': x['title'], 'last_update': x['last_update']}
                for x in dashboard_db.get_datasets(username)]
    return render_template('dashboard.html', username=username, desc=desc, datasets=datasets)


@bp.route('/users/<username>/update', methods=('POST',))
def update(username):
    data_post = request.get_json()
    if data_post is None: abort(400)
    # authorization
    if 'api_secret' not in data_post or database.auth.get_user(username)['api_secret'] != data_post['api_secret']:
        return 'WRONG_API_SECRET', 403
    for k, v in data_post['payload'].items():
        assert (len(k) == 8)
        dashboard_db.update_dataset_data(username, int(k, 16), json.dumps(v))

    logging.getLogger(__name__).info('Dashboard updated. Username = ' + username)
    return '', 204


@bp.route('/users/<username>/dashboard/add', methods=('POST',))
def add(username):
    if username != g.user['username']:
        abort(403)
    dashboard_db.append_dataset(username, title=request.form['datasetName'])
    return redirect(url_for('dashboard_manager.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard/remove', methods=('POST',))
def remove(username):
    if username != g.user['username']:
        abort(403)
    dashboard_db.remove_dataset(username, idx=int(request.form['id'], 16))
    return redirect(url_for('dashboard_manager.show_dashboard', username=username))


@bp.route('/users/<username>/dashboard/edit_layout/<dataset>', methods=('GET', 'POST'))
def edit_layout(username, dataset):
    assert(isinstance(dataset, str))
    dataset = int(dataset, 16)

    delegate = DatasetDelegate(username, dataset)
    if g.user is None or username != g.user['username']:
        abort(403)
    if request.method == 'GET':
        return render_template('edit_layout.html', dataset=delegate)
    elif request.method == 'POST':
        layout_old = delegate.layout
        try:
            delegate.layout = request.form['layout']
            delegate.render()
        except json.JSONDecodeError as e:
            delegate.layout = layout_old
            return json.dumps({'status': 'json_error', 'exception': e.__dict__})
        except IndexError:
            delegate.layout = layout_old
            return json.dumps({'status': 'renderer_error'})
        except SyntaxError:
            delegate.layout = layout_old
            return json.dumps({'status': 'py_syntax_error'})
        except KeyError:
            delegate.layout = layout_old
            return json.dumps({'status': 'key_error'})
        return json.dumps({'status': 'success'})
    else:
        abort(400)
