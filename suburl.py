from flask import Blueprint, session, current_app

from login_check import apply_login_check, login_check_exempt, user

sub = Blueprint('sub', __name__)

apply_login_check(sub)

@sub.route(r'/authored_test/', methods=['GET'])
def authored_test():
    return 'authorized url'


@login_check_exempt
@sub.route(r'/test/', methods=['GET'])
def test():
    current_app.logger.debug('session.permanent: %s.' % session.permanent)
    return 'test'


