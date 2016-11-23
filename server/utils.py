import pickle
import settings
import graph


def load_graph(path):
    with open(path, 'rb') as raw_data:
        graph = pickle.load(raw_data)

    return graph


# prepare_for_view: article,
# prepare_for_view_left_items: title
def strip_element(items, title, length):
    for item in items:
        if len(item[title]) < length:
            continue

        item[title] = item[title][:length] + "..."

    return items


from functools import wraps

from flask import Response, current_app, request


def check_auth(username, password):
    creds = current_app.config['ADMIN_CREDENTIALS'].split(',')
    return username == creds[0] and password == creds[1]


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

keys = {
    'SOCIAL_TWITTER': {
        'consumer_key': 'twitter consumer key',
        'consumer_secret': 'twitter consumer secret'
    },
    'SOCIAL_FACEBOOK': {
        'consumer_key': 'XXXXX',
        'consumer_secret': 'XXXXX',
        'request_token_params': {'scope': 'email,publish_stream'}
    }
}
# TODO nb change flask_social update_recursive to items instead of iteritems
def init_config(app):
    for k, v in keys.items():
        app.config[k] = v
