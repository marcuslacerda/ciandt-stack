"""Script clean project."""
import logging
from config import Config
from knowledge import Knowledge, Project
from stack import Stack
from utils import logger_builder

try:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sheet_id',
        help='Define the sheet_id',
        required=True)
    parser.add_argument(
        '--notify',
        action='store_true',
        default=False,
        help='If notify is defined, then errors will be sent by email',
        required=False)
    parser.add_argument(
        '--logging_level', default='ERROR',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level of detail.')
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

sheet_id = args['sheet_id'] or None
logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

config = Config()
knowledge = Knowledge(config)
project = Project(config)
stack = Stack(config)

project.delete_by_query("sheet_id:"+sheet_id)
knowledge.delete_by_query("sheet_id:"+sheet_id)
stack.delete_by_query('key:'+sheet_id)
