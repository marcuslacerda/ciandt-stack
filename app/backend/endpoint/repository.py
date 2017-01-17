"""Repository class for people index."""
from elasticsearch import Elasticsearch
import logging
import os
import json
from utils import database

logger = logging.getLogger('profile')


class Repository(object):

    def __init__(self, config):
        host = config['ELASTICSEARCH_URL']
        user = config['ELASTICSEARCH_USER']
        password = config['ELASTICSEARCH_PASS']

        self.es = database.initEs(host, user, password)
        logger.debug('Connecting on %s' % (host))


    def create_template_if_notexits(self, index):
        """If template doesn't exists, create one from json file definition.

        Method reads a template definition from file on path ./resources
        ('%s-template.json' % index) where index is a method's parameter.
        """
        if not self.es.indices.exists_template(name=index):
            resource_path = os.path.join(
                os.path.split(__file__)[0],
                ("resources/%s-template.json" % index))
            with open(resource_path) as data_file:
                settings = json.load(data_file)

            # create index
            response = self.es.indices.put_template(name=index, body=settings)
            logger.debug("Template %s created" % response['acknowledged'])

    def search_data_by_query(self, index, doc_type, query, size=2500):
        data = self.es.search(index=index, doc_type=doc_type, body=query, size=size)

        list_data = []
        for item in data['hits']['hits']:
            list_data.append(item['_source'])
        return list_data


    def search_by_query(self, index, doc_type, query, size=2500):
        return self.es.search(index=index, doc_type=doc_type, body=query, size=size)

    def insert(self, index, doc_type, login, document):
        res = self.es.index(index=index, doc_type=doc_type, body=document, id=login)
        logger.debug("Created documento ID %s" % res['_id'])

        return res

    def update (self, index, doc_type, id, body):
        return self.es.update(index=index, doc_type=doc_type, id=id, body=body)

    def get_document(self, index, doc_type, id, source=None):
        if source:
            return self.es.get(index=index, doc_type=doc_type, id=id, _source=source)
        else:
            return self.es.get(index=index, doc_type=doc_type, id=id)
