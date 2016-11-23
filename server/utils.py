from functools import wraps
from flask import Response, current_app, request
from settings import *

import pickle
import settings
import graph


def load_graph(path):
    with open(path, 'rb') as raw_data:
        graph = pickle.load(raw_data)

    return graph


def strip_element(items, title, length):
    for item in items:
        if len(item[title]) < length:
            continue

        item[title] = item[title][:length] + "..."

    return items


def check_auth(username, password):
    credentials = current_app.config['ADMIN_CREDENTIALS'].split(',')
    return username == credentials[0] and password == credentials[1]


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


# TODO nb change flask_social update_recursive to items instead of iteritems
def init_config(app):
    for k, v in keys.items():
        app.config[k] = v
