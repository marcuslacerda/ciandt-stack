"""Project class."""
import logging
from utils import database
from techgallery import TechGallery
import techgallery

logger = logging.getLogger('stack')
index = 'project'
doc_type = 'settings'

DEFAULT_IMG_URL = 'https://techgallery.ciandt.com/assets/images/placeholder.png'


class Project(object):
    """Profile operations."""

    def __init__(self, config):
        """Init profile object using config param."""
        host = config.get('PROJECT_ELASTICSEARCH_HOST')
        user = config.get('PROJECT_ELASTICSEARCH_USER')
        password = config.get('PROJECT_ELASTICSEARCH_PASS')
        logger.debug('test %s at user %s with %s pass' % (host, user, password))
        self.es = database.initEs(host, user, password)
        self.tc = TechGallery(config)
        logger.debug('Connecting on %s for %s' % (host, index))

    def find_by_sheet_id(self, sheet_id=None):
        """Return project by sheet_id or return all if sheet_id is none."""
        if sheet_id:
            query = {"query": {"match": {"sheet_id": sheet_id}}}
        else:
            query = {"query": {"match_all": {}}}

        return self.es.search(index=index, body=query, size=1000)


    def find_all(self):
        """Retrieve all documents."""
        query = '{"query": {"match_all": {}}}'
        return self.es.search(index=index, body=query, size=3000)

    def save(self, doc, refresh=False):
        """Save profile document. Create template if it not exists."""
        database.create_template_if_notexits(self.es, __file__, index)
        logger.debug(doc)
        res = self.es.index(
            index=index,
            doc_type=doc_type,
            body=doc,
            id=doc['sheet_id'],
            refresh=refresh)
        logger.debug("Created documento ID %s" % res['_id'])

        return res

    def delete(self, id):
        """Remove documento by id."""
        self.es.delete(index=index, doc_type=doc_type, id=id)

    def delete_by_query(self, search, number=10):
        """Delete all documents match with search expresstion."""
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
                # Git the next page of results.
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

    def get_technology_list(self, sheet_id):
        """Retrieve a list of tecnologies from sheet_id."""
        query = {
            "query": {"match": {
               "sheet_id": sheet_id
            }}
        }

        stack = []
        data = self.es.search(index=index, body=query, size=1)

        for project in data['hits']['hits']:
            item = project['_source']

            if 'stack' not in item:
                logger.warning('spreadsheet %s with no stack' % sheet_id)
                continue

            for tech in item['stack']:
                tech_name = tech
                if tech_name:
                    tech_key = techgallery.convert_name_to_id(tech_name)
                    image = DEFAULT_IMG_URL

                    # workaround: techgallery image has no pattern for url name
                    (tc_tech, status_code) = self.tc.technology(tech_key)
                    if 'image' in tc_tech:
                        logger.debug(tc_tech['image'])
                        image = tc_tech['image']
                    else:
                        logger.debug('technology not found %s' % tc_tech)

                    doc_tech = {
                        "technology": tech_key,
                        "technologyName": tech_name,
                        "imageUrl": image
                    }
                    # add new tech definition
                    stack.append(doc_tech)

        return stack

    def get_team(self, sheet_id):
        """Get list logins (team) from spreadsheet id."""
        query = {
            "query": {
                "match": {
                    "sheet_id": sheet_id
                }
            }
        }

        team = []

        data = self.es.search(index=index, body=query, size=1)

        for project in data['hits']['hits']:
            item = project['_source']

            logger.debug(item)

            if 'team' in item:
                for login in item['team']:
                    doc = {
                        "login": login,
                        "email": '%s@ciandt.com' % login,
                        "image": "https://citweb.cit.com.br/ipeople/photo?cdLogin=%s" % login
                    }
                    team.append(doc)

        return team

    def get_last_10m_activity(self):
        # get spreadsheets updated from 10 minutos ago to now
        query = {"query": {"range": {"@timestamp": {"gte": "now-10m", "lt":  "now"}}}}
        return self.es.search(index='archboard', body=query, size=20)
