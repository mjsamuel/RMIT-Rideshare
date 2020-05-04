from flask import Blueprint, jsonify
from flask import current_app as app

api = Blueprint("api", __name__, url_prefix='/api')

@api.route('/login')
def login():
    ret_value = {'message': 'Correct credentials'}
    return jsonify(ret_value)

@api.route('/register')
def register():
    ret_value = {'message': 'Account created'}
    return jsonify(ret_value)
