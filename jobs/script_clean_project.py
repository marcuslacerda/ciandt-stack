"""Script clean project."""
import logging
from config import Config
from knowledge import Knowledge, Project

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

config = Config()
knowledge = Knowledge(config)
project = Project(config)

sheet_id = '1NZeRcbswSQbKHgDw8cT0CuWe7-0q8M5YrWlkTbXYnwo'

q = "sheet_id:"+sheet_id
project.delete_by_query('project', q)
knowledge.delete_by_query('knowledge', q)
# stack.delete_by_query('stack', 'key:'+sheet_id)
