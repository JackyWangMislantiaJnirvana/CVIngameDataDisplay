from flask import *


bp = Blueprint('errorhandler', __name__)


@bp.app_errorhandler(404)
def not_found(e):
    return render_template('error_page/not_found.html'), 404


@bp.app_errorhandler(403)
def forbidden(e):
    return render_template('error_page/forbidden.html'), 403


@bp.app_errorhandler(500)
def ise(e):
    return render_template('error_page/ise.html'), 500
