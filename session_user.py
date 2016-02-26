from werkzeug.datastructures import CallbackDict
from flask import session, abort

class SessionUser(object):
    """
        Used to acces user info in session.
        In fact, it is just a proxy of session object.
        Changes to user info will saved after request handling (SessionInterface.save_session).
    """
    def __init__(self, session):
        self.session = session

    # proxy of dict-specific template methods
    def __getitem__(self, key):
        return self.session[key]

    def __setitem__(self, key, value):
        self.session[key] = value

    def __delitem__(self, key):
        del self.session[key]

    # proxy of public methods and members
    def __getattr__(self, key):
        return getattr(self.session, key)




def session_user(app, user_check=None):
    @app.before_request
    def get_user():
        user = SessionUser(session)
        app.user = user     # improvement: make it in request context

        if user_check is not None:
            if not user_check(user):
                abort(401)  # http 401 -> unauthorized


# ----- sample of login check ----
from flask import current_app, request

_login_check_exempts = []

def login_check_exempt(view):
    global _login_check_exempts
    _login_check_exempts.append(view)
    return view


def login_check(user):
    global _login_check_exempts
    view = current_app.view_functions.get(request.endpoint)
    if not view in _login_check_exempts:
        return False    # you should check user here
