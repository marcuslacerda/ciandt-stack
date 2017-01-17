"""Trends backend."""
from backend import app, logger
from flask_restplus import Namespace, Resource, fields
from repository import Repository
from utils import security


api = Namespace('trends', description='Trends operations')
# api.add_resource(PeopleList, '/hello')

trend = api.model('Trend', {
    'name': fields.String(
        description=u'The name of bucket',
        required=True,
    ),
    'count': fields.Integer(
        description=u'The value of bucket',
        required=True,
    )
})

repository = Repository(app.config)
index='stack'
doc_type='setting',

@api.route('/owners')
class OwnerTrendsList(Resource):
    """OwnerTrendsList Operations."""

    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(trend)
    def get(self, user=None):
        """List the 15 top owners."""
        query = build_query_trends_owners(15)
        data = search_aggs_by_query(query)
        return data


@api.route('/technologies')
class TechsTrendsList(Resource):
    """TechsTrendsList Operations."""

    @api.doc(security='oauth2')
    @security.login_authorized
    @api.marshal_list_with(trend)
    def get(self, user=None):
        """List the top 15 technolgies."""
        query = build_query_trends_technologies(15)
        data = search_aggs_by_query(query)

        return data

def build_query_trends_owners(size):
    query = {
        "size": 0,
        "aggs": {
            "owners": {
              "terms": {
                "field": "owner.raw",
                "size": size,
                "order": {
                  "_count": "desc"
                }
              }
            }
        }
    }

    return query

def build_query_trends_technologies(size):
    query = {
        "size": 0,
        "aggs": {
            "owners": {
              "terms": {
                "field": "stack.technologyName.raw",
                "size": size,
                "order": {
                  "_count": "desc"
                }
              }
            }
        }
    }

    return query


def search_aggs_by_query(query):
    data = repository.search_by_query(index=index, doc_type=doc_type, query=query)

    list_trends = []
    for item in data['aggregations']['owners']['buckets']:
      doc = {
        'name' : item['key'],
        'count': item['doc_count']
      }
      list_trends.append(doc)

    return list_trends
