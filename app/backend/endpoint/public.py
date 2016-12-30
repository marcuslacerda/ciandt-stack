from backend import app
from backend.version import __version__
from flask import jsonify
import logging
# TODO: refactory and remove this imports
from elasticsearch import Elasticsearch
from connection import UrlFetchAppEngine

config = {'elasticsearch' : app.config['ELASTICSEARCH_URL']}

logger = logging.getLogger('stack')


@app.route('/api/public/version', methods = ['GET'])
def api_version():
    return jsonify(__version__)


@app.route('/api/public/whoknows', methods = ['GET'])
def api_whoknows_get():
    q = request.args.get('q')
    top = request.args.get('top') or 10
    r = Database(config)

    query = {
      "sort" : [
          { "endorsementsCount" : "desc" },
          { "skillLevel" : "desc"}
      ],
      "query": {
          "query_string": {
             "query": q
          }
      }
    }

    data = r.search_by_query(index="skill", query=query, size=top)

    list_stack = []
    for item in data['hits']['hits']:
        list_stack.append(item['_source'])

    return jsonify(list_stack)


@app.route('/api/public/whichprojectuses', methods = ['GET'])
def api_whichprojectuses_get():
    q = request.args.get('q')
    top = request.args.get('top') or 10
    r = Database(config)

    query = {
      "sort" : [
          { "achieve" : "desc" }
      ],
      "query": {
          "query_string": {
             "query": q
          }
      }
    }

    data = r.search_by_query(index="knowledge", query=query, size=top)

    list_stack = []
    for item in data['hits']['hits']:
        list_stack.append(item['_source'])

    return jsonify(list_stack)


class Database(object):
    def __init__(self, config):
        self.es = Elasticsearch(
        [config['elasticsearch']],
        connection_class=UrlFetchAppEngine,
        send_get_body_as='POST')

    def save_document(self, index, document_type, document, id=None):
        res = self.es.index(index=index, doc_type=document_type, body=document, id=id)
        logger.debug("Created documento ID %s" % res['_id'])

    def search_by_query(self, index, query, size):
        """
        Sample of query: {"query": {"match_all": {}}}
        """
        resp = self.es.search(index=index, body=query, size=size)
        logger.debug("%d documents found" % resp['hits']['total'])

        return resp
