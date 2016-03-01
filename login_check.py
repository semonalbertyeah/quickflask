from flask import current_app, request, abort
from werkzeug.routing import NotFound

from session_user import apply_session_user

"""
    login_check samples:
"""

# 2 test users
test_uesrs = {
    'admin': '123456', 
    'guest': '111111'
    }


_login_check_exempts = []

def login_check_exempt(view):
    global _login_check_exempts
    _login_check_exempts.append(view)
    return view


def login_check(user):
    global _login_check_exempts
    view = current_app.view_functions.get(request.endpoint)
    if view is None:
        abort(404)  # not found
    if view in _login_check_exempts:
        return True

    # no username and password in session
    if not user.has_key('username') or \
       not user.has_key('password'):
        return False

    passwd =  user.get(user['username'], None)
    if passwd:
        if passwd == user['password']:
            return True
        else:
            return False
    else:
        return False


def apply_login_check(app):
    apply_session_user(app, user_check=login_check)


from session_user import user
