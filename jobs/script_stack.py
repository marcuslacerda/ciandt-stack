"""Script file for Knowledge Map.

Sample:
# help command
python script_stack.py --help

# process all projects
python script_stack.py --full
"""
import logging
from stack import Stack
from knowledge import Knowledge
from config import Config

# logging definitions
FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)

config = Config()
stack = Stack(config)
knowledge = Knowledge(config)

try:
    import argparse
    parser = argparse.ArgumentParser()
    # parser.add_argument('--sheet_id', help='Define the sheet_id', required=False)
    parser.add_argument('--full', action='store_true', default=False, help='Option full process all project. Otherwise, only projects that not exists on stack index.', required=False)
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

# sheet = args['sheet_id'] or None
full = args['full'] or False
if full:
    projects = knowledge.list_aggregations_tkci_per_flow()
else:
    projects = [item for item in knowledge.list_aggregations_tkci_per_flow() if not stack.exists(item['key'])]

logger.info('%s projects ' % len(projects))
stack.create_template_if_notexits()
for project in projects:
    key = project['key']
    # add technologies list
    logger.info('starting %s' % key)
    stack.load_stack(project)
