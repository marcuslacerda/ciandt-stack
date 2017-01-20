"""Skill class."""
import logging
from utils import database

index = 'skill'
doc_type = 'technology'

logger = logging.getLogger('stack')


class Skill(object):
    """Init skill object."""

    def __init__(self, config):
        """Init object."""
        host = config.get('SKILL_ELASTICSEARCH_HOST')
        user = config.get('SKILL_ELASTICSEARCH_USER')
        password = config.get('SKILL_ELASTICSEARCH_PASS')
        self.es = database.initEs(host, user, password)
        logger.debug('Connecting on %s for %s' % (host, index))

    def save(self, doc):
        """Save skill document. Create template if it not exists."""
        database.create_template_if_notexits(self.es, __file__, index)
        res = self.es.index(index=index, doc_type=doc_type, body=doc)
        logger.debug("Created documento ID %s" % res['_id'])

        return res

    def delete_all(self):
        """Delete all documents."""
        self.es.indices.delete(index=index)
