#!/usr/bin/env python3

from flask import Flask, render_template, redirect, request, current_app, session, \
    flash, url_for, make_response, jsonify
from flask_security import LoginForm, current_user, login_required, \
    login_user
from flask_social.utils import get_provider_or_404
from flask_social.views import connect_handler
from flask_social import Social, SQLAlchemyConnectionDatastore
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager
from flask_assets import Environment

from flask_sqlalchemy import SQLAlchemy
from search import *
from settings import *
from utils import *
from suggestions import get_suggest

from forms import RegisterForm
from flask_assets import Bundle
import models
from utils import requires_auth
import database

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/test.db'
app.secret_key = 'SupaDupaSecretKey'

webassets = Environment(app)
webassets.config['sass_bin'] = '/usr/local/bin/sass'

js_libs = Bundle('js/libs/jquery-1.7.1.min.js',
                 'js/libs/bootstrap.min.js',
                 filters='jsmin',
                 output='js/libs.js')

js_main = Bundle('js/src/main.js',
                 filters='jsmin',
                 output='js/main.js')

css_less = Bundle('css/src/styles.less',
                  filters='less',
                  output='css/styles.css',
                  debug=False)

css_main = Bundle(Bundle('css/bootstrap.min.css'),
                  css_less,
                  filters='cssmin',
                  output='css/main.css')

webassets.cache = not app.debug
app.config['ASSETS_DEBUG'] = True

webassets.register('js_libs', js_libs)
webassets.register('js_main', js_main)
webassets.register('css_main', css_main)

agent = search()
graph = load_graph(GRAPH_PATH)
API = None


def getApi():
    global API
    if API is None:
        API = Api(app)
    return API


@app.before_first_request
def before_first_request():
    from database import init_db
    try:
        init_db(app)
    except Exception as e:
        app.logger.error(str(e))


@app.route('/')
def index():
    query = request.args.get('query')
    search_results = []
    if query is not None and len(query) > 0:
        search_results = agent.request(query)

    search_results = strip_element(search_results, 'abstract', POST_MAX_LENGTH)
    response = make_response(render_template('index.html', search_results=search_results, history=[], suggestion=[]))
    response.set_cookie('history', '', expires=0)

    if query is not None and len(query) > 0:
        response.set_cookie('query', query)
    if current_user.is_authenticated:
        log = models.Log(current_user.id, query)
        db.session.add(log)
        db.session.commit()
    return response


@app.route('/references')
def references():
    paper_id = request.args.get('id', '')

    try:
        paper_id = int(paper_id)
    except ValueError:
        return render_template('index.html', search_results=[], suggestion=[])

    if current_user.is_authenticated:
        log = models.Click(current_user.id, paper_id)
        db.session.add(log)
        db.session.commit()

    references = graph.adj_list(paper_id)
    papers = []
    if len(references) > 0:
        papers = agent.papers(references)

    history = []
    if request.cookies.get('history') is not None:
        history = request.cookies.get('history').split(',')
    if str(paper_id) not in history:
        history.append(str(paper_id))
    query = request.cookies.get('query')
    path = get_suggest(graph, paper_id, 10, query)
    history_papers, suggestion_papers = strip_element(agent.papers(history), 'title',
                                                      LEFT_BLOCK_LENGTH), strip_element(agent.papers(path), 'title',
                                                                                        LEFT_BLOCK_LENGTH)
    response = make_response(
        render_template('index.html', search_results=papers, history=history_papers, suggestion=suggestion_papers))
    response.set_cookie('history', ','.join(history))
    return response


@app.route('/graph')
def draw_graph():
    paper_id = request.args.get('id', '')
    try:
        paper_id = int(paper_id)
    except ValueError:
        return render_template('index.html', search_results=[], suggestion=[])

    nodes, edges = point_neighborhoods(graph, paper_id, DRAW_RADIUS)
    articles = agent.papers(nodes)
    articles_id = list(map(lambda x: x['id'], articles))
    edges = list(filter(lambda x: x[0] in articles_id or x[1] in articles_id, edges))
    return jsonify(nodes=articles, edges=edges)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(request.referrer or '/')

    return render_template('login.html', form=LoginForm())


@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<provider_id>', methods=['GET', 'POST'])
def register(provider_id=None):
    if current_user.is_authenticated:
        return redirect(request.referrer or '/')

    form = RegisterForm()

    if provider_id:
        provider = get_provider_or_404(provider_id)
        connection_values = session.get('failed_login_connection', None)
    else:
        provider = None
        connection_values = None

    if form.validate_on_submit():
        ds = current_app.security.datastore
        user = ds.create_user(email=form.email.data, password=form.password.data)
        ds.commit()

        # See if there was an attempted social login prior to registering
        # and if so use the provider connect_handler to save a connection
        connection_values = session.pop('failed_login_connection', None)

        if connection_values:
            connection_values['user_id'] = user.id
            connect_handler(connection_values, provider)

        if login_user(user):
            ds.commit()
            flash('Account created successfully', 'info')
            return redirect(url_for('profile'))

        return render_template('thanks.html', user=user)

    login_failed = int(request.args.get('login_failed', 0))
    return render_template('register.html',
                           form=form,
                           provider=provider,
                           login_failed=login_failed,
                           connection_values=connection_values)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
                           twitter_conn=current_app.social.twitter.get_connection(),
                           facebook_conn=current_app.social.facebook.get_connection())


@app.route('/profile/<provider_id>/post', methods=['POST'])
@login_required
def social_post(provider_id):
    message = request.form.get('message', None)

    if message:
        provider = get_provider_or_404(provider_id)
        api = provider.get_api()

        if provider_id == 'twitter':
            display_name = 'Twitter'
            api.PostUpdate(message)
        if provider_id == 'facebook':
            display_name = 'Facebook'
            api.put_object('me', 'feed', message=message)

        flash('Message posted to %s: %s' % (display_name, message), 'info')

    return redirect(url_for('profile'))


@app.route('/admin')
@requires_auth
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/admin/users/<user_id>', methods=['DELETE'])
@requires_auth
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'info')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    init_config(app)
    security_ds = SQLAlchemyUserDatastore(db, models.User, models.Role)
    social_ds = SQLAlchemyConnectionDatastore(db, models.Connection)

    app.security = Security(app, security_ds)
    app.social = Social(app, social_ds)
    app.run()
