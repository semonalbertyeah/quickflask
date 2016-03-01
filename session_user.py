from werkzeug.datastructures import CallbackDict
from werkzeug.local import LocalProxy
from flask import session, abort, _request_ctx_stack

class SessionUser(object):
    """
        Used to acces user info in session.
        SessionUser is a proxy of session object.
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

    # proxy of public methods and members (readonly)
    # **note:
    #   __getattr__ gets called when __getattribute__ raise AttributeError,
    #   which means only the attribute which is not found in self will be accessed on self.session.
    #   Since object has no public methods or attributes, you can access all public methods and attrs of session.
    def __getattr__(self, key):
        return getattr(self.session, key)

    # note here: do not override __delattr__ and __setattr__ like above



def apply_session_user(app, user_cls=SessionUser, user_check=None):
    @app.before_request
    def get_user():
        user = user_cls(session)
        _request_ctx_stack.top.user = user     # 

        if user_check is not None:
            if not user_check(user):
                abort(401)  # http 401 -> unauthorized

def _get_user():
    return getattr(_request_ctx_stack.top, 'user', None)

user = LocalProxy(_get_user)


# ----- sample of login check ----
# usr: admin:123456
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
        try:
            if user['username'] == 'admin' and \
                user['password'] == '123456':
                return True
            else:
                return False
        except KeyError:
            return False


