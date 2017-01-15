"""People Endpoint."""
from backend import app, logger
from flask import request
from flask_restplus import Namespace, Resource, fields
from repository import Repository
from utils import security


api = Namespace('stacks', description='Stack operations')
# api.add_resource(PeopleList, '/hello')

userData = api.model('UserData', {
    'image': fields.String(
        description=u'The URL of the user profile',
        required=False,
    ),
    'login': fields.String(
        description=u'The unique id for user account',
        required=True,
    ),
    'email': fields.String(
        description=u'The email address',
        required=True,
    ),
})

stack = api.model('Stack', {
    'key': fields.String(readOnly=True, description='The unique identifier'),
    'name': fields.String(required=True, description='Full name'),
    'owner': fields.String(required=True, description='Owner of this stack'),
    'index': fields.Float(required=False, description='Index of compliance. Range from 0 to 1'),
    # 'like_count': fields.Integer(required=False, description='Index of compliance. Range from 0 to 1'),
    'last_activity': fields.DateTime(required=False, description='Date of last activity on stack'),
    'last_activity_user': fields.String(required=True, description='User login that was responsible for last activity'),
    'stack': fields.List(
        fields.Nested(api.model('TechnolgyData', {
            'imageUrl': fields.String(
                description=u'Url for technology icon',
                required=False,
            ),
            'technology': fields.String(
                description=u'Technolgy id',
                required=True,
            ),
            'technologyName': fields.String(
                description=u'Technolgy of area',
                required=True,
            ),
        }))
    ),
    'team': fields.List(fields.Nested(userData)),
})

# query = api.model('Query DSL', {
#     'query': fields.String,
# })

parser = api.parser()
parser.add_argument('q', type=int, help='Query param for method GET', location='query')

repository = Repository(app.config)

index='stack'
doc_type='setting',

@api.route('/_search')
@api.response(401, 'Authorization header not defined')
@api.response(403, 'Authorization token with error')
class StackSearch(Resource):
    """Shows a list of all people, and lets you POST to add new tasks"""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.expect(parser)
    @api.marshal_list_with(stack)
    def get(self, user):
        """Simple search of stacks."""
        query = {
            "sort": [
               {
                  "last_activity": {
                     "order": "desc"
                  }
               }
            ],
            "query": {
                "query_string": {
                   "query": request.args.get('q')
                }
            }
        }
        logger.debug('query %s' % query)

        return repository.search_data_by_query(index=index, doc_type=doc_type, query=query)


@api.route('/')
@api.response(401, 'Authorization header not defined')
@api.response(403, 'Authorization token with error')
class StackList(Resource):
    """Shows a list of all people, and lets you POST to add new tasks."""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(stack)
    def get(self, user):
        """List all stacks."""
        query = {
            "sort": [
               {
                  "last_activity": {
                     "order": "desc"
                  }
               }
            ],
            "query": {
                "match_all": {}
            }
        }
        return repository.search_data_by_query(index=index, doc_type=doc_type, query=query)


@api.route('/team/<key>')
class StackTeam(Resource):
    """Shows a list of all people, and lets you POST to add new tasks."""
    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(userData)
    def get(self, user, key):
        """List all team of stack."""
        stack = repository.get_document(
            index=index,
            doc_type=doc_type,
            id=key,
            source='team.*')
        return stack['_source']['team']
