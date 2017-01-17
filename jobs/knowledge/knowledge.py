"""Knowledge class."""
import logging
from utils import database
import time

logger = logging.getLogger('stack')
index = 'knowledge'
doc_type = 'tech'


class Knowledge(object):
    """Profile operations."""

    def __init__(self, config):
        """Init profile object using config param."""
        host = config.get('KNOWLEDGE_ELASTICSEARCH_HOST')
        user = config.get('KNOWLEDGE_ELASTICSEARCH_USER')
        password = config.get('KNOWLEDGE_ELASTICSEARCH_PASS')
        self.es = database.initEs(host, user, password)
        logger.debug('Connecting on %s for %s' % (host, index))

    def find_all(self):
        """Retrieve all documents."""
        query = '{"query": {"match_all": {}}}'
        return self.es.search(index=index, body=query, size=3000)

    def save(self, doc, refresh=False):
        """Save profile document. Create template if it not exists."""
        database.create_template_if_notexits(self.es, __file__, index)
        res = self.es.index(
            index=index,
            doc_type=doc_type,
            body=doc,
            refresh=refresh)
        logger.debug("Created documento ID %s" % res['_id'])

        return res

    def bulk_save(self, documents):
        """Save all documents."""
        # TODO: change to bulk operation
        for doc in documents:
            res = self.es.index(
                index=index,
                doc_type=doc_type,
                body=doc)
            logger.debug("Created documento ID %s" % res['_id'])

    def load_spreadsheet_knowledge_map(self, spreadsheet_api, service, spreadsheet, notify=False):
        """Load data from spreadsheet api and save on knowledge database."""
        item = spreadsheet

        spreadsheetId = item['_source']['sheet_id']
        owner = item['_source']['update_by']
        last_activity = item['_source']['@timestamp']
        flow = item['_source']['flow']
        contract = item['_source']['contract']
        logger.debug('processing spreadsheet: %s ' % spreadsheetId)
        rangeName = 'TC_Report!A2:K'

        skill_index = 0

        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
        values = result.get('values', [])
        if not values:
            logger.warn('No data found.')
        else:
            items = spreadsheet_api.read_sheet_data(spreadsheetId, values)
            logger.debug('%s technologies on this spreadsheet ' % len(items))

            skill_index = sum(int(items['skill_index']) for i in items)
            logger.debug('skill index is %s ' % skill_index)
            # refresh flow and contract values from TC_Report sheet
            flow = items[0]['flow']
            contract = items[0]['contract']

            q = "sheet_id:"+spreadsheetId
            database.create_template_if_notexits(self.es, __file__, index)
            self.delete_by_query(q)
            self.bulk_save(items)
            logger.info('==> spreadsheet %s loads successfully ' % spreadsheetId)

        # sum index skill_index

        doc = {
            "key": spreadsheetId,
            "owner": contract,
            "name": flow,
            "last_activity_user": owner,
            "last_activity": last_activity,
            "index": 0
        }

        # TODO: this sleep was needed to avoid Insufficient
        # tokens for quota group and limit 'ReadGroupUSER-100s'
        time.sleep(2)
        return doc


    def delete(self, id):
        """Remove documento by id."""
        self.es.delete(index=index, doc_type=doc_type, id=id)

    def delete_by_query(self, search, number=10):
        """Delete all documents match with search expresstion."""
        if self.es.indices.exists_type(index=index, doc_type=doc_type):
            hits = self.es.search(
                q=search,
                index=index,
                _source="_id",
                size=number,
                search_type="scan",
                scroll='5m')
            logger.debug('Deleting %s records... ' % hits['hits']['total'])

            # Now remove the results.
            while True:
                try:
                    # Get the next page of results.
                    scroll = self.es.scroll(
                        scroll_id=hits['_scroll_id'],
                        scroll='5m', )

                    # We have results initialize the bulk variable.
                    bulk = ""

                    # Remove the variables.
                    for result in scroll['hits']['hits']:
                        bulk = bulk + '{ "delete" : { "_index" : "' + str(result['_index']) + '", "_type" : "' + str(result['_type']) + '", "_id" : "' + str(result['_id']) + '" } }\n'

                    self.es.bulk(body=bulk)
                except Exception:
                    break

    def list_aggregations_tkci_per_flow(self):
        """Get a sum aggregation TKCI per flow."""
        query = {
          "size": 0,
          "query": {
            "query_string": {
              "query": "*",
              "analyze_wildcard": "true"
            }
          },
          "aggs": {
            "sheets": {
              "terms": {
                "field": "sheet_id.raw",
                "size": 0,
                "order": {
                  "_count": "desc"
                }
              },
              "aggs": {
                "contract": {
                  "terms": {
                    "field": "contract.raw",
                    "order": {
                      "_count": "desc"
                    }
                  },
                  "aggs": {
                    "flow": {
                      "terms": {
                        "field": "flow.raw",
                        "order": {
                          "_count": "desc"
                        }
                      },
                      "aggs": {
                        "tkci": {
                          "sum": {
                            "field": "skill_index"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }

        projects = []

        data = self.es.search(index=index, body=query, size=0)

        for item in data['aggregations']['sheets']['buckets']:

            key = item['key']
            contract = item['contract']['buckets'][0]
            flow = contract['flow']['buckets'][0]
            tkci = flow['tkci']['value']

            doc = {
                "key": key,
                "owner": contract['key'],
                "name": flow['key'],
                "index": tkci
            }

            projects.append(doc)
        return projects
