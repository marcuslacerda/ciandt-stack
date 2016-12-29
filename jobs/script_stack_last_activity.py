"""Script file for Knowledge Map.

Sample:
# help command
python script_stack_last_activity.py --help

# process all spreadsheets and notify errors by email
python script_stack_last_activity.py --notify
"""
from config import Config
from google import Spreadsheet, GMail
from stack import Stack
from knowledge import Knowledge, Project
from oauth2client import tools
from apiclient import errors
from utils import logger_builder

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument(
        '--notify',
        action='store_true',
        default=False,
        help='If notify is defined, then errors will be sent by email',
        required=False)
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

notify = args['notify'] or False

config = Config()
spreadsheet_api = Spreadsheet(flags)
knowledge = Knowledge(config)
project = Project(config)
stack = Stack(config)
gmail = GMail(flags)

service = spreadsheet_api.get_service_spreadsheets()
spreadsheets = project.get_last_10m_activity()
logger.info('total %s sheets' % spreadsheets['hits']['total'])

for item in spreadsheets['hits']['hits']:
    spreadsheetId = item['_source']['sheet_id']
    owner = item['_source']['update_by']
    flow = item['_source']['flow']
    contract = item['_source']['contract']

    logger.info('starting %s' % spreadsheetId)

    logger.info('=> loading sheet knowledge_map')
    try:
        project = knowledge.load_spreadsheet_knowledge_map(
            spreadsheet_api,
            service,
            item,
            notify
        )

        logger.info('=> loading stack')
        stack.load_stack(project)
    except errors.HttpError, err:
        if err.resp.status in [404, 500]:
            # delete sheet_id from index project and knowledge index
            q = "sheet_id:"+spreadsheetId
            project.delete_by_query(q)
            knowledge.delete_by_query(q)
            logger.warning("==> Spreadsheet %s doesn't exists: %s" % (spreadsheetId, err))
        else:
            # send email to owner
            logger.error("==> exception on %s : %s" % (spreadsheetId, err))
            if notify:
                subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
                gmail.send(owner, subject, spreadsheetId, str(err))
    except Exception, e:
        logger.error("==> exception on %s : %s" % (spreadsheetId, e))
        if notify:
            subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
            gmail.send(owner, subject, spreadsheetId, str(e))

logger.info('spreadsheet process finished')
