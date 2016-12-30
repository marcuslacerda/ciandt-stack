from backend import app, logger
from flask import Blueprint
from flask_restplus import Api

from stack import api as api_stack
from auth import api as api_auth
from user import api as api_user
import public
import trends

blueprint = Blueprint('api', __name__, url_prefix='/api')

authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    version='1.0',
    title='Stack API',
    description='Access stack data.',
    authorizations=authorizations)

app.register_blueprint(blueprint)
api.add_namespace(api_stack)
logger.info('Profile API was registered.')
api.add_namespace(api_auth)
logger.info('Auth API was registered.')
api.add_namespace(api_user)
logger.info('User API was registered.')
