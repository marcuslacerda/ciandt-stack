from server import app, logger
from server.security import login_authorized

import requests
from flask import jsonify
import logging
from elasticsearch import Elasticsearch

from connection import UrlFetchAppEngine

config = {'elasticsearch' : app.config['ELASTICSEARCH_URL']}

@app.route('/api/trends/owners')
@login_authorized
def api_trends_owners(user):
  database = Database(config)

  return jsonify(database.search_trends_owners(15))

@app.route('/api/trends/technologies')
@login_authorized
def api_trends_technologies(user):
  database = Database(config)

  return jsonify(database.search_trends_technologies(10))

class Database(object):
  def __init__(self, config):
    self.es = Elasticsearch(
        [config['elasticsearch']],
        connection_class=UrlFetchAppEngine,
        send_get_body_as='POST')


  def search_trends_owners(self, size):
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

    return self.search_aggs_by_query(query)

  def search_trends_technologies(self, size):
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

    return self.search_aggs_by_query(query)


  def search_aggs_by_query(self, query):
    index = 'stack'
    data = self.es.search(index=index, body=query)

    list_trends = []
    for item in data['aggregations']['owners']['buckets']:
      doc = {
        'name' : item['key'],
        'count': item['doc_count']
      }
      list_trends.append(doc)

    return list_trends
