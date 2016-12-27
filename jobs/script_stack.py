"""Script file for Knowledge Map.

Sample:
# help command
python script_stack.py --help

# process all projects
python script_stack.py --full
"""
from stack import Stack
from knowledge import Knowledge
from config import Config
from utils import logger_builder

config = Config()
stack = Stack(config)
knowledge = Knowledge(config)

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--full',
        action='store_true',
        default=False,
        help='Option full process all project. ' +
        'Otherwise, only projects that not exists on stack index.',
        required=False)
    parser.add_argument(
        '--logging_level', default='ERROR',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level of detail.')

    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

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
