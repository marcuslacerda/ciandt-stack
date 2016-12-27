"""Script file for Knowledge Map.

Sample:
# help command
python script_stack_last_activity.py --help

# process all spreadsheets and notify errors by email
python script_stack_last_activity.py --notify
"""
import logging
from config import Config
from google import Spreadsheet
from stack import Stack
from knowledge import Knowledge, Project
import google as send_gmail
from oauth2client import tools
from apiclient import errors

FORMAT = '%(name)s %(levelname)-5s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('stack')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.DEBUG)
logging.getLogger('elasticsearch').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.http').setLevel(logging.ERROR)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('--notify', action='store_true', default=False, help='If notify is defined, then errors will be sent by email', required=False)
    flags = parser.parse_args()
    args = vars(flags)
except ImportError:
    flags = None

notify = args['notify'] or False

config = Config()
spreadsheet_api = Spreadsheet(flags)
knowledge = Knowledge(config)
project = Project(config)
stack = Stack(config)

service = spreadsheet_api.get_service_spreadsheets()
spreadsheets = project.get_last_10m_activity()
logger.info('total %s sheets' % spreadsheets['hits']['total'])

for spreadsheet in spreadsheets['hits']['hits']:
    logger.info('starting %s' % spreadsheet['_source']['sheet_id'])

    logger.info('=> loading sheet knowledge_map')
    try:
        project = knowledge.load_spreadsheet_knowledge_map(
            spreadsheet_api,
            service,
            spreadsheet,
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
                send_gmail.send(owner, subject, spreadsheetId, str(err))
    except Exception, e:
        logger.error("==> exception on %s : %s" % (spreadsheetId, e))
        if notify:
            subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
            send_gmail.send(owner, subject, spreadsheetId, str(e))

logger.info('spreadsheet process finished')
