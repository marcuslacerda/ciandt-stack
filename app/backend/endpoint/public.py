from backend import app, logger
from flask import request
from backend.version import __version__
from flask_restplus import Namespace, Resource, fields
from repository import Repository
from utils import security


api = Namespace('public', description='Public operations')
# api.add_resource(PeopleList, '/hello')

skill = api.model('Skill', {
    'name': fields.String(
        description=u'The complete name',
        required=True,
    ),
    'login': fields.String(
        description=u'The unique login of user',
        required=True,
    ),
    'city': fields.String(
        description=u'The name of bucket',
        required=True,
    ),
    'skillLevel': fields.Integer(
        description=u'Skill evaluation level',
        required=True,
    ),
    'endorsementsCount': fields.Integer(
        description=u'Total of endorsements from another users',
        required=True,
    )
})

knowledge = api.model('knowledge', {
    'flow': fields.String(
        description=u'Flow where this technology has been used.',
        required=True,
    ),
    'technology': fields.String(
        description=u'Technology name as a tech gallery system',
        required=True,
    ),
    'achieve': fields.Integer(
        description=u'Total achievement for this technology',
        required=True,
    )
})

parser = api.parser()
parser.add_argument('q', required=True, help='Query param for method GET', location='query')

repository = Repository(app.config)

@api.route('/version')
class VersionList(Resource):
    """VersionList Operations."""

    def get(self):
        """Show versions details."""
        return __version__


@api.route('/whoknows')
class WhoknowsList(Resource):
    """WhoknowsList Operations."""

    @api.expect(parser)
    @api.marshal_list_with(skill)
    def get(self):
        """List who knows a specific tecnology.

        Result is ordered by endorsementsCount and skillLevel.
        """
        q = request.args.get('q')
        top = request.args.get('top') or 10
        query = {
          "sort": [
              { "endorsementsCount": "desc" },
              { "skillLevel": "desc"}
          ],
          "query": {
              "query_string": {
                 "query": q
              }
          }
        }

        data = repository.search_data_by_query(
            index="skill",
            doc_type="technology",
            query=query,
            size=top)

        return data

@api.route('/whichprojectuses')
class WhichProjectUsesList(Resource):
    """Whichprojectuses Operations."""

    @api.expect(parser)
    @api.marshal_list_with(knowledge)
    def get(self):
        """List which project is using a specific tecnology.

        Result is ordered by achieve.
        """
        q = request.args.get('q')
        top = request.args.get('top') or 10

        query = {
          "sort": [
              {"achieve": "desc"}
          ],
          "query": {
              "query_string": {
                 "query": q
              }
          }
        }

        data = repository.search_data_by_query(
            index="knowledge",
            doc_type="tech",
            query=query,
            size=top)

        return data
