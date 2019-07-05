import os
import logging

from flask import Flask, render_template, send_from_directory

from server import auth, dashboard_manager, users, errorhandler, docs
from server.database import close_database, get_database
from server.renderer.renderer_registry import registry as renderer_registry

app = Flask(__name__, template_folder="templates-zh_CN")
# app = Flask(__name__)
app.config.from_pyfile('config.py')

# blueprint
app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(dashboard_manager.bp)
app.register_blueprint(errorhandler.bp)
app.register_blueprint(docs.bp)

# renderer
renderer_registry.register_renderer_list()

# teardown registry
app.teardown_appcontext(close_database)

# logger config
logging.basicConfig(
    filename=app.config["LOGFILE"],
    format="%(levelname)-10s %(asctime)s %(message)s",
    level=logging.INFO
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.before_first_request
def first_use():
    if not os.path.isfile(os.path.join(app.root_path, app.config['DATABASE'])):
        logging.info("No Database! Creating...")
        from server.database import auth
        db = get_database()
        db.executescript(open(os.path.join(app.root_path, 'schema.sql')).read())
        db.commit()
        code = auth.append_invite_code()[1]
        pw = auth.generate_strong_password()
        auth.create_user(username='admin', password=pw, code=code, admin=True)
        logging.info("Database initialized. Admin info:")
        logging.info("USERNAME: admin")
        logging.info(f"PASSWORD: {pw}")
    else:
        logging.info("DB Detected")