from functools import wraps
from flask import session, request, redirect, url_for

def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if kwargs.get('code', None) != 'abcd':
            return jsonify({'data':"Wrong code", 'status':'error'})

        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(session.get('user'), request.url)
        if session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function