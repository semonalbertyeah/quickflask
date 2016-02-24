import os, json

from flask import Flask
from flask import url_for
from flask import render_template
from flask import request, session
from flask import make_response, redirect, abort

from sqlite_session import SqliteSessionInterface

# Flask-Session -> flask_session.Session
from flask.ext.session import Session
# Flask-SQLAlchemy -> flask_sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy


# if __name__ == '__main__':
#   flask will take some action
app = Flask(__name__)


# load config (config.py -> class Config)
app.config.from_object('config.Config')

# for sqlite session
session_dir = 'sessions'
if app.config.has_key('SQLITE_SESSION_DIR'):
    session_dir = app.config['SQLITE_SESSION_DIR']
app.sql_session_interface = SqliteSessionInterface(session_dir)

# init Flask-SQLAlchemy
db = SQLAlchemy(app)

# update config['SESSION_SQLALCHEMY'] for Flask-Session (default to None)
#app.config['SESSION_SQLALCHEMY'] = db
app.config.update(SESSION_SQLALCHEMY=db)

# init Flask-Session
# after initiation, session will be 
Session(app)


# =========== steps before request handling ===========
@app.before_request
def step1():
    app.logger.debug('step1')
    abort(401)


@app.before_request
def step2():
    app.logger.debug('step2')
    #return 'intercepted by step2 of before_request' # this will intercept reuest handling


# ==== steps after request handling ====
@app.after_request
def after_step1(response):
    app.logger.debug(repr(response))
    return response


# ======== url rules ========
@app.route('/')
def index():
    resp = make_response('Index page.')
    app.logger.debug('app.session_cookie_name: %s' % app.session_cookie_name)
    return resp
    #return "Index Page."


# ======== variable url rules ========
# url param is passed as  show_user(username="admin")
@app.route('/user/<username>/')
def show_user(username):
    return "User %s" % username

# variable with type restriction
# available types:
#   int -> integer
#   float -> floating point number
#   path -> like the default but also accept slash 
@app.route('/post/<int:post_id>/')
def show_post(post_id):
    return "Post %d" % post_id


# ======== unique urls / redirection behavior ========
# Flask's URL rules are based on Werkseug's routing module.
# url should end with a trailing slash
# and if access without a trailing slash, 
# it will be added automatically(redirect)


# ======== url building ========
def test_url_building():
    with app.test_request_context():
        app.logger.debug(url_for('index'))
        
        # url with parameter
        app.logger.debug(url_for('show_user', username="admin"))
        
        # extra value will be appended as querystring
        app.logger.debug(url_for('show_post', post_id=33, extra="extra_value"))
        
        # static url
        app.logger.debug(url_for('static', filename='style.css'))


# ======== HTTP methods in url rule ========
# supported methods:
#   GET  -> just get
#   HEAD -> GET without content (only http header)
#   POST -> data stored only once
#   PUT  -> server might trigger the store precedure multiple times
#           by overwriting the old values.
#   DELETE  ->  remove info at the give location
#   OPTIONS ->  used to figure out supported methods of a url.
@app.route('/get_post/', methods=['GET', 'POST'])
def get_post():
    if request.method == 'POST':
        return 'post request'
    else:
        return 'get request'

# ======== static files ========
# create dir static
# url "/static/*" will access files in static dir

# ======== tempalte ========
# flask use Jinja2
# create dir templates
# template files will be searched in templates
# below is accessible in template:
#   request, session, g obj, get_flashed_messages func
# *note:
#   g obj is something in whicn you can store information for your own needs.

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



# ======== request ========
# by global flask.request object
# which is context locals -> thread safe
@app.route('/login/', methods=['POST', 'GET'])
def login():
    err = None
    app.logger.debug(dict(request.args))    # access querystring params
    if request.method == 'POST':
        # if password or username not in request.form:
        #   -> KeyError -> HTTP 404 (automatically)
        if request.form['username'] == 'admin' \
            and request.form['password'] == '123456':
            return 'logged in.'
        else:
            err = "invalid username or password"

    return render_template('login.html', error=err)


# ======== file uploads ========
@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']   # the_file -> name of the file field
        f.save(os.path.join('uploaded', f.filename))
        return 'file uploaded'
    elif request.method == 'GET':
        return render_template('upload_file.html')
    else:
        return "not supported method for url: /upload/"




# ======== cookie ========
# flask.request.cookies
@app.route('/show_cookies/')
def show_cookies():
    return json.dumps(request.cookies)

@app.route('/set_cookies/')
def set_cookies():
    resp = make_response(render_template('cookies.html', info="add cookie"))
    resp.set_cookie('test_cookie', 'This is test cookie value.')
    return resp

@app.route('/del_cookies/')
def del_cookies():
    resp = make_response(render_template('cookies.html', info='delete cookie'))
    resp.set_cookie('test_cookie', '', expires=0)   # set expiration to 1970
    return resp
    

# ======== redirect and errors ========
@app.route('/redirect/')
def redirect_handler():
    app.logger.debug('redirect')
    return redirect(url_for('abort_handler'))

@app.route('/abort/')
def abort_handler():
    app.logger.debug('abort')
    #abort(404) # this will  return http 404 page as response


# ======== custom error page ========
@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A custom header'
    return resp


# ======== response ========
# view return response obj -> return it directly
# view return string -> response obj is created with string and default params
# view return tuple -> tuple must be in the form of (response, status, headers)
#                      where:
#                           status -> override the status code
#                           headers -> list or dict of additional header values


# ======== sessions ========
# by default, FLask session is stored in signed cookies
@app.route('/show_session/')
def show_session():
    return json.dumps(dict(session), indent=4)

@app.route('/set_session/')
def set_session():
    session['test'] = 'test session value'
    return 'set session value'

@app.route('/del_session/')
def del_session():
    session.pop('test', None)
    return 'delete session value'


# ======== sqlite session ====
@app.route('/show_sql_session/')
def show_sql_session():
    # error here:
    #   if no sessionid in cookie, new session will always be created.
    session = app.sql_session_interface.open_session(app, request)
    return json.dumps(dict(session), indent=4)
 
@app.route('/set_sql_session/')
def set_sql_session():
    session = app.sql_session_interface.open_session(app, request)
    session['test'] = 'just a test value'
    resp = make_response('set sql session test')
    app.sql_session_interface.save_session(app, session, resp)
    return resp

@app.route('/del_sql_session/')
def del_sql_session():
    session = app.sql_session_interface.open_session(app, request)
    del session['test']
    resp = make_response('delete sql session test')
    app.sql_session_interface.save_session(app, session, resp)
    return resp

# ======= flask_kvsession ======

# ======= Flask-Session =========
@app.route('/flask_session_get/')
def flask_session_get():
    return session.get('key', 'not set')

@app.route('/flask_session_set/')
def flask_session_set():
    session['key'] = 'value'
    return 'ok'


if __name__ == '__main__':
    # debug mode:
    #   changed code will be reload automatically
    #   traceback will be shown on web page.
    # enable:
    #   app.debug=True
    #   or
    #   app.run(debug=True)
    #app.debug = True
    app.logger.debug(app.session_cookie_name)
    app.run(host='0.0.0.0', debug=True)
    #test_url_building()

