"""Script clean project."""
import logging
from config import Config
from knowledge import Knowledge, Project
from stack import Stack

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

config = Config()
knowledge = Knowledge(config)
project = Project(config)
stack = Stack(config)

sheet_id = '18AjKn8CJwH1yErnJU6DP7waIdPFtYpJqpMLcZgu84Tc'

project.delete_by_query("sheet_id:"+sheet_id)
knowledge.delete_by_query("sheet_id:"+sheet_id)
stack.delete_by_query('key:'+sheet_id)
