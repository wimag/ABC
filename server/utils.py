from functools import wraps
from flask import Response, current_app, request
from settings import *
from collections import deque

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


def point_neighborhoods(graph, point, radius):
    nodes = [point]
    edges = []

    queue = deque([(point, 0)])
    while len(queue) != 0:
        daddy, length = queue.popleft()
        if length >= radius:
            continue

        neighbours = list(map(lambda x: (x, length + 1), graph.adj_list(point)))
        for child, length in neighbours:
            edges.append((daddy, child))
            nodes.append(child)

        queue += neighbours

    return nodes, edges
