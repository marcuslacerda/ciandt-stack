"""User info API operations."""
from backend import logger
from utils import security
from flask_restplus import Namespace, Resource, fields

api = Namespace('users', description='User operations')

user = api.model('User', {
    'email': fields.String(readOnly=True, description="The email address"),
    'family_name': fields.String(required=True, description='Full name'),
    'gender': fields.String(required=True, description='The gender of user. Might be male or famale'),
    'given_name': fields.String(required=True, description='First name'),
    'hd': fields.String(required=True, description='The hosted G Suite domain of the user'),
    'sub': fields.String(required=True, description='The unique id for user account'),
    'profile': fields.String(required=True, description='Full link for google+ profile'),
    'locale': fields.String(required=True, description='The locate'),
    'name': fields.String(required=True, description='The full name of user, in a displayable form'),
    'access_token': fields.String(required=True, description='A token that can be sent to a Google API'),
    'picture': fields.String(required=True, description='The URL of the profile picture'),
    'email_verified': fields.String(required=True, description='True if the e-mail address has been verified; otherwise false')
})

""" Exemplo:
{
  "email": "mlacerda@ciandt.com",
  "family_name": "Lacerda",
  "gender": "male",
  "given_name": "Marcus",
  "hd": "ciandt.com",
  "sub": "108374356961407507632",
  "picture": "https://plus.google.com/+MarcusLacerda",
  "locale": "en",
  "name": "Marcus Lacerda",
  "access_token": "OAuth ya29.CjC1A2Lr_XxdJTBRYT6r3gxTCHP89ks_jWcb__scduE3PQR6ZUXwpYuLVPSZhFkSvi4",
  "picture": "https://lh4.googleusercontent.com/-dVKbcz6Y6iI/AAAAAAAAAAI/AAAAAAAABXA/7wg55gy_qZc/photo.jpg",
  "email_verified": true
}
"""


@api.route('/me')
@api.response(401, 'Authorization header not defined')
@api.response(403, 'Authorization token with error')
class UserInfo(Resource):
    """User info resources."""

    @security.login_authorized
    @api.marshal_with(user)
    def get(self, user):
        """Retrieve the logged user details.

        Return a user model if the authorization code were defined in a header.
        Return error otherwise
        """
        logger.info('Call user info %s' % user['email'])
        return user
