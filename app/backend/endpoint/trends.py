from backend import app, logger
import requests
from flask import jsonify
import logging
from elasticsearch import Elasticsearch
from repository import Repository
from utils import security

from connection import UrlFetchAppEngine

repository = Repository(app.config)

index='stack'
doc_type='setting',


@app.route('/api/trends/owners')
# @security.login_authorized
def api_trends_owners(user=None):
    query = build_query_trends_owners(15)
    data = search_aggs_by_query(query)
    return jsonify(data)

@app.route('/api/trends/technologies')
# @security.login_authorized
def api_trends_technologies(user):
    query = build_query_trends_technologies(15)
    data = search_aggs_by_query(query)

    return jsonify(data)

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
