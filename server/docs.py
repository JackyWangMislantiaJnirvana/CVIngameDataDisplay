from flask import Blueprint, render_template, request, abort

bp = Blueprint('docs', __name__)


class Document:
    def __init__(self, html_name, incl_path, title):
        self.html_name = html_name
        self.incl_path = incl_path
        self.title = title


docs = [
    Document('update', 'docs/update.html', 'Update'),
    Document('basic-layout', 'docs/basic_layout.html', 'Basic Layout'),
    Document('renderer', 'docs/renderer.html', 'Renderer')
]


@bp.route('/docs/')
def docs_list():
    return render_template('docs/index.html', docs=docs)


@bp.route('/docs/getdoc.cgi')
def getdoc():
    doc_id = 0
    try:
        doc_id = int(request.args['doc'])
    except ValueError:
        abort(400)

    if doc_id < len(docs):
        return render_template(docs[doc_id].incl_path)
    else:
        abort(400)
