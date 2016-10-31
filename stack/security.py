from flask import redirect, url_for, session
from flask import request, abort
from functools import wraps
from httplib2 import Http
import json

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        print ( '==> login_required: ' + str(access_token))
        if access_token is None:
          print ('==> not logged')
          return redirect(url_for('signin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def login_authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @authorized
    def secured_root(userid=None):
        pass
    """

    def _wrap(*args, **kwargs):
        if 'Authorization' not in request.headers:
            # Unauthorized
            print("No token in header")
            abort(401)
            return None

        print("Checking token...")
        authorization = request.headers['Authorization']
        print ('==> %s' % authorization )
        userid = validate_token(authorization)
        if userid is None:
            print("Check returned FAIL!")
            # Unauthorized
            abort(401)
            return None

        return fn(userid=userid, *args, **kwargs)
    return _wrap    

# put this in for example gauth.py
# ref: http://flask.pocoo.org/snippets/125/
def validate_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an e-mail on success'''
    h = Http()
    resp, cont = h.request("https://www.googleapis.com/oauth2/v2/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': access_token})

    print cont

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    return data['email']