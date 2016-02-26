from flask import current_app, request
from werkzeug.routing import NotFound

_login_check_exempts = []

def login_check_exempt(view):
    global _login_check_exempts
    _login_check_exempts.append(view)
    return view


def login_check(user):
    global _login_check_exempts
    try:
        view = current_app.view_functions.get(request.endpoint)
        if view in _login_check_exempts:
            return True
    except NotFound:
        pass

    print '---- check view:', view
    try:
        user['password']
        user['username']
    except KeyError:
        return False
    else:
        return True
