"""People Endpoint."""
from backend import app, logger
from flask import request
from flask_restplus import Namespace, Resource, fields
from repository import Repository
from utils import security
import elasticsearch

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

parser = api.parser()
parser.add_argument('q', required=True, help='Query param for method GET', location='query')

repository = Repository(app.config)

index='stack'
doc_type='setting',

@api.route('/_search')
@api.response(401, 'Authorization header not defined')
@api.response(403, 'Authorization token with error')
class StackSearch(Resource):
    """StackSearch Operations."""

    @api.doc(security='oauth2')
    @security.login_authorized
    @api.expect(parser)
    @api.marshal_list_with(stack)
    def get(self, user):
        """Search stack by query param. Query is passed by 'q' URL param.."""
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
    """StackList Operations."""

    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(stack)
    def get(self, user):
        """List all available stacks ordered by last-update field."""
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

@api.route('/<id>')
@api.response(404, 'Stack not found')
@api.param('id', 'The stack identifier')
class Stack(Resource):
    """Show a single stack item and lets you delete them"""
    @api.doc('get_stack')
    @security.login_authorized
    @api.marshal_with(stack)
    def get(self, user, id):
        """Fetch a given resource."""
        stack = repository.get_document(index=index, doc_type=doc_type, id=id)
        return stack['_source']

    @api.doc('delete_stack')
    @security.login_authorized
    @api.response(204, 'Stack deleted')
    def delete(self, user, id):
        """Delete a stack given its login identifier."""
        query = "sheet_id %s" % id
        print "FIND BY ID"
        try:
            stack = repository.get_document(index=index, doc_type=doc_type, id=id)
            print stack
            repository.delete_by_id(index=index, doc_type=doc_type, id=id)
            repository.delete_by_query(index="knowledge", search=query)
            repository.delete_by_query(index="project", search=query)

            return '', 204
        except elasticsearch.NotFoundError as e:
            return '', 404

    @api.expect(stack)
    @security.login_authorized
    @api.marshal_with(stack)
    def put(self, user, id):
        """Update a task given its identifier."""
        print request.json
        repository.insert(index=index, doc_type=doc_type, id=id, document=request.json)
        return request.json

@api.route('/team/<key>')
class StackTeam(Resource):
    """StackTem Operations."""

    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(userData)
    def get(self, user, key):
        """Get a team for stack id.

        A team is a list of users with email, login and image-url.
        """
        stack = repository.get_document(
            index=index,
            doc_type=doc_type,
            id=key,
            source='team.*')
        return stack['_source']['team']
