from backend import app, logger

from flask import jsonify, request
from functools import wraps
from httplib2 import Http
import requests
import json
import jwt
from jwt import DecodeError, ExpiredSignature

VALID_EMAIL_DOMAIN = '@ciandt.com'


def login_authorized(fn):
    """Decorator that checks that requests
    contain an id-token in the session or request header.
    userid will be None if the
    authentication failed, and have an id otherwise.

    Usage:
    @app.route("/")
    @auth.login_authorized
    def secured_call(userid=None):
        pass
    """
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        logger.debug('=== Authorization check ===')
        if 'Authorization' in request.headers:
            logger.debug('=== Check Authorization token')
            access_token = request.headers.get('Authorization').split()[1]
            user = validate_token(access_token)
            if user is not None:
                return fn(user=user, *args, **kwargs)

            response = jsonify(message='Check access token failed')
            response.status_code = 403
            return response

        # try parser json web token
        if 'jwt-authorization' in request.headers:

            logger.debug('=== Check JWT Authorization')
            try:
                json_web_token = parse_token(request)

                if 'user' in json_web_token:
                    logger.debug("Getting user from JWT TOKEN ===>")
                    return fn(user=json_web_token['user'], *args, **kwargs)

                access_token = get_oauth_token(json_web_token)
                logger.debug('=== access_token: %s' % access_token)

                logger.debug('=== Getting user data from google by access_token')
                user = validate_token(access_token)
                if user is not None:
                    return fn(user=user, *args, **kwargs)

                response = jsonify(message='Check access token failed')
                response.status_code = 403
                return response

            except DecodeError:
                response = jsonify(message='Token is invalid')
                response.status_code = 401
                return response
            except ExpiredSignature:
                # try_dispach_whti_refresh_token(fn, *args, **kwargs)
                response = jsonify(message='JSON Web Token has expired')
                response.status_code = 403
                return response

        response = jsonify(message='Missing authorization header')
        response.status_code = 401
        return response

    return decorated_function


def try_dispach_whti_refresh_token(fn, *args, **kwargs):
    json_web_token = parse_token_no_validade(request)
    logger.debug('=== Trying to refresh access_token')
    if 'refresh_token' in json_web_token['user']:
        refresh_token = json_web_token['user']['refresh_token']
        logger.debug('=== Refresh access_token using %s' % refresh_token)
        new_token = refresh_access_token(refresh_token)
        logger.debug('=== Getting user by access_token')
        user = validate_token(new_token['access_token'])

        if user is not None:
            return fn(user=user, *args, **kwargs)
        else:
            logger.debug('=== Refresh access_token not work')

def revoke_token(access_token):
    h = Http(disable_ssl_certificate_validation=True)
    logger.debug('revoking %s' % access_token)
    resp, cont = h.request('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': 'Bearer %s' % access_token})

    return resp

def refresh_access_token(refresh_token):
    """"Refresh access_token"""
    payload = dict(grant_type='refresh_token',
                   client_id=app.config['GOOGLE_CLIENT_ID'],
                   client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                   refresh_token=refresh_token)
    # h = Http(disable_ssl_certificate_validation=True)
    # resp, cont = h.request(
    #     "https://www.googleapis.com/oauth2/v3/userinfo",
    #     method='POST',
    #     body=json.dumps(payload),
    #     )

    logger.debug(payload)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post(
        "https://accounts.google.com/o/oauth2/token",
        data=payload,
        headers=headers)

    logger.debug('=====> %s' % r.status_code)

    if not r.status_code == 200:
        return None

    logger.debug(r.text)
    return json.loads(r.text)

def validate_token(access_token):
    '''Verifies that an access-token is valid and
    meant for this app.

    Returns None on fail, and an User on success'''
    h = Http(disable_ssl_certificate_validation=True)
    resp, cont = h.request("https://www.googleapis.com/oauth2/v3/userinfo",
                           headers={'Host': 'www.googleapis.com',
                                    'Authorization': 'Bearer %s' % access_token})

    if not resp['status'] == '200':
        return None

    try:
        data = json.loads(cont)
    except TypeError:
        # Running this in Python3
        # httplib2 returns byte objects
        data = json.loads(cont.decode())

    data['oauth_token'] = access_token

    return data

def get_oauth_token(json_web_token):
    access_token =  json_web_token['access_token']

    if access_token:
        return access_token
    return None


def create_token(payload):
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token.decode('unicode_escape')

def parse_token_no_validade(req):
    options = {
        'verify_exp': False,
    }
    token = req.headers.get('jwt-authorization').split()[1]
    return jwt.decode(token, app.config['SECRET_KEY'], options=options)


def parse_token(req):
    # raise ExpiredSignature('Token was expired.')
    token = req.headers.get('jwt-authorization').split()[1]
    return jwt.decode(token, app.config['SECRET_KEY'])


def response_not_authorized(status, error):
    response = jsonify({'code': status,'message': error})
    response.status_code = status
    return response

def is_valid_email(email):
    return VALID_EMAIL_DOMAIN in email
