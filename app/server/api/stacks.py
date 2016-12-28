from server import app, logger
from server.version import __version__
from server import security

from flask import jsonify
from flask import request
import logging
from elasticsearch import Elasticsearch
from connection import UrlFetchAppEngine

config = {'elasticsearch' : app.config['ELASTICSEARCH_URL']}

@app.route('/api/stacks/', methods = ['GET'])
@security.login_authorized
def api_stack(user):
	r = Database(config)

	return jsonify(r.list_stack())

@app.route('/api/stacks/search', methods = ['GET'])
@security.login_authorized
def api_stack_search(user):
	q = request.args.get('q')
	r = Database(config)

	return jsonify(r.search_stack(q))

@app.route('/api/stacks/<id>', methods = ['GET'])
@security.login_authorized
def api_stack_id(user, id):
	source = request.args.get('_source')
	r = Database(config)

	return jsonify(r.get_stack(id, source))

@app.route('/api/stacks/team/<id>', methods = ['GET'])
@security.login_authorized
def api_team(user, id):
	source='team.*'
	r = Database(config)
	stack = r.get_stack(id, source)

	return jsonify(stack['_source']['team'])

@app.route('/api/stacks/<id>', methods = ['POST'])
@security.login_authorized
def api_stack_post(user, id):
	payload = request.json

	return id, 200


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

	def search_stack(self, q):
		query = {
		    "query": {
		        "query_string": {
		           "query": q
		        }
		    }
		}
		logger.debug('query %s' % query)

		data = self.search_by_query('stack', query, 2500)
		list_stack = []
		for item in data['hits']['hits']:
			list_stack.append(item['_source'])

		return list_stack


	def list_stack(self):
		index = 'stack'
		data = self.es.search(index=index, body={"query": {"match_all": {}}}, size=2500, sort='last_activity:desc')
		list_stack = []
		for item in data['hits']['hits']:
			stack = item['_source']
			stack['like_count'] = 0
			list_stack.append(item['_source'])

		return list_stack

	def get_stack(self, id, source):
		if source:
			return self.es.get(index='stack', doc_type='setting', id=id, _source=source)
		else:
			return self.es.get(index='stack', doc_type='setting', id=id)
