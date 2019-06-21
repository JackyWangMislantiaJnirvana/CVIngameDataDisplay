import os

from flask import *

from server import auth
from server import dashboard_manager
from server import users
from server.database import close_database
from server.renderer.renderer_registry import registry as renderer_registry

app = Flask(__name__)
app.config.from_pyfile('config.py')

# blueprint
app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(dashboard_manager.bp)

# renderer
renderer_registry.register_renderer_list()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.teardown_appcontext(close_database)
    app.run(debug=True)  # TODO: DELETE BEFORE DEPLOYMENT
