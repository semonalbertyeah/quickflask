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

    if user.new:
        current_app.logger.error('no session')
        return False

    # no username and password in session
    if not user.has_key('username') or \
       not user.has_key('password'):
        current_app.logger.error('no username or password in session')
        return False

    passwd =  test_uesrs.get(user['username'], None)
    if passwd:
        if passwd == user['password']:
            return True
        else:
            current_app.logger.error('wrong password for user "%s"' % user['username'])
            return False
    else:
        current_app.logger.error('no password for user "%s"' % user['username'])
        return False


def apply_login_check(app_or_blueprint):
    apply_session_user(app_or_blueprint, user_check=login_check)


from session_user import user
