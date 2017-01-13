"""People Endpoint."""
from backend import logger, app
from utils import security
from flask import request
from flask_restplus import Namespace, Resource, fields
from flask import jsonify
import requests
import json
from datetime import datetime
from repository import Repository

repository = Repository(app.config)

index='profile'
doc_type='google',

api = Namespace('auth', description='Authentication operations')

user = api.model('User', {
    'login': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Full name'),
})

payload = api.model('Payload json', {
    'json': fields.String,
})


@api.route('/google')
class GoogleProvider(Resource):
    """Shows a list of all people, and lets you POST to add new tasks"""
    # Using OAuth 2.0 to Access Google APIs. Login flow
    # https://developers.google.com/identity/protocols/OAuth2
    # https://developers.google.com/identity/protocols/OpenIDConnect#exchangecode
    # Step 1: (Browser) Send an authentication request to Google
    # Step 2: Exchange authorization code for access token.
    # Step 3: Retrieve information about the current user.
    @api.expect(payload)
    def post(self):
        """List all people."""
        access_token_url = 'https://www.googleapis.com/oauth2/v4/token'
        people_api_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
        tokeninfo_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'

        logger.debug('google request =>')
        logger.debug(request.json)

        payload = dict(client_id=request.json['clientId'],
                       redirect_uri=request.json['redirectUri'],
                       client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                       code=request.json['code'],
                       grant_type='authorization_code')

        logger.debug('Google Payload =>')
        logger.debug(payload)

        # Step 2. Exchange authorization code for access token.
        r = requests.post(access_token_url, data=payload)
        token = json.loads(r.text)
        logger.debug('Access Token =>')
        logger.debug(token)

        # Step 2. Retrieve information about the current user.
        # create user if not exists one
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
        r = requests.get(people_api_url, headers=headers)
        profile = json.loads(r.text)
        logger.info('Login as => %s' % profile['email'])
        logger.debug(profile)

        if security.is_valid_email(profile['email']):
            # Step 4. Create a new account or return an existing one.
            r = requests.get('%s?access_token=%s' % (tokeninfo_url, token['access_token']))
            token_info = json.loads(r.text)
            logger.debug('Tokeninfo =>')
            logger.debug(token_info)

            # Step 5. Sign-up a user process
            account = {}
            try:
                account = repository.get_document(
                    index=index,
                    doc_type=doc_type,
                    id=profile['sub'])

            except Exception as e:
                account = profile
                logger.debug('First logging for  %s' % profile['email'])
                if 'refresh_token' in token:
                    profile['refresh_token'] = token['refresh_token']

                repository.insert(index=index, doc_type=doc_type, login=profile['sub'], document=profile)

            # Step 6. Create a new account or return an existing one.
            account['iat'] = datetime.utcnow()
            account['exp'] = token_info['exp']
            account['access_token'] = token['access_token']
            # payload = {
            #     'sub': profile['sub'],
            #     'iat': datetime.utcnow(),
            #     'exp': token_info['exp'],
            #     'access_token':token['access_token']
            # }
            jwt = security.create_token(account)
            return jsonify(token=jwt)
        else:
            return not_authorized(403, 'Invalid email domain. Please sign with ciandt.com acccount')


@api.route('/logout')
class LogoutProvider(Resource):
    @security.login_authorized
    def get(user):
        """Revoke access token for user."""
        logger.info('Logout by %s' % user['email'])
        access_token = user['oauth_token']
        security.revoke_token(access_token)

        return "Logout Success", 200

def not_authorized(status, error):
    response = jsonify({'code': status,'message': error})
    response.status_code = status
    return response
