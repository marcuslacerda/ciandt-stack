"""Stack class."""
import logging
from utils import database
from knowledge import Project

logger = logging.getLogger('stack')
index = 'stack'
doc_type = 'setting'


class Stack(object):
    """Stack operations."""

    def __init__(self, config):
        """Init stack object."""
        host = config.get('STACK_ELASTICSEARCH_HOST')
        user = config.get('STACK_ELASTICSEARCH_USER')
        password = config.get('STACK_ELASTICSEARCH_PASS')
        self.es = database.initEs(host, user, password)
        logger.debug('Connecting on %s for %s' % (host, index))
        self.project = Project(config)

    def load_stack(self, project):
        """Load technology list and team to save stack.

        Project must have a structure like this:
        doc = {
            "key": - id
            "owner" :
            "name" :
            "index" :
        }
        """
        key = project['key']

        # merge attr transational of stack if they weren't defined
        if 'last_activity' not in project:
            try:
                doc_result = self.es.get(index="stack", doc_type="setting", id=key)
                if '_source' in doc_result:
                    doc_stack = doc_result['_source']
                    project['last_activity'] = doc_stack.get('last_activity')
                    project['last_activity_user'] = doc_stack.get('last_activity_user')
                    logger.debug('merge was done')
            except Exception, e:
                logger.info('stack %s not exits' % key)

        # add technologies list
        techs = self.project.get_technology_list(key)
        project['stack_size'] = len(techs) if techs else 0
        project['stack'] = techs
        # add team members
        team = self.project.get_team(key)
        project['team_size'] = len(team) if team else 0
        project['team'] = team
        # save document
        self.save_document(project, key)

        return project

    def create_template_if_notexits(self):
        """Create template if not exists."""
        database.create_template_if_notexits(self.es, __file__, index)

    def save_document(self, document, id=None):
        """Save stack document."""
        res = self.es.index(index=index, doc_type=doc_type, body=document, id=id)
        logger.debug("Created documento ID %s" % res['_id'])
        return res

    def exists(self, id):
        """Return true if documento id is found."""
        return self.es.exists(index=index, doc_type=doc_type, id=id)

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
