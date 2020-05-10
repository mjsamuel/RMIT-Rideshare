import os

from flask import Blueprint, send_from_directory

docs = Blueprint("docs", __name__)

@docs.route('/docs/<path:filename>')
def web_docs(filename):
    """Endpoint to view Sphinx documentation easily within the Flask app

    .. :quickref: Other; View Sphinx documentation.
    """
    directory = os.path.join(
        os.path.dirname(__file__),
        os.pardir,
        os.pardir,
        os.pardir,
        'docs/_build/html')
    print(directory)
    print(filename)


    return send_from_directory(directory, filename)
