"""Script file for Knowledge Map.

Sample:
# help command
python script_knowledgemap.py --help

# process all spreadsheets and notify errors by email
python script_knowledgemap.py --notify

# process just spreadsheets sheet_id and not notify errors
# load just sheet_id
python script_knowledgemap.py --sheet_id 1tsmRA0TOCEpr5aAQA8-B4CQ8jk0WtiVhiYNu8JK8YDQ
"""
from config import Config
from google import Spreadsheet, GMail
from knowledge import Knowledge, Project
from oauth2client import tools
from apiclient import errors
from utils import logger_builder

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument(
        '--sheet_id',
        help='Define the sheet_id',
        required=False)
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

sheet = args['sheet_id'] or None
notify = args['notify'] or False
logging_level = args['logging_level'] or 'ERROR'
logger = logger_builder.initLogger(logging_level)

config = Config()
spreadsheet_api = Spreadsheet(flags)
knowledge = Knowledge(config)
project = Project(config)
gmail = GMail(flags)


def load_knowledge_map(sheet=None, notify=False):
    """Load data from spreadsheet api and save on knowledge database."""
    # authenticate and get service API for spreadsheet
    service = spreadsheet_api.get_service_spreadsheets()
    spreadsheets = project.find_by_sheet_id(sheet)

    total_hits = spreadsheets['hits']['total']
    logger.info('total %s sheets' % total_hits)
    total_errs = 0

    for item in spreadsheets['hits']['hits']:
        spreadsheetId = item['_source']['sheet_id']
        owner = item['_source']['update_by']
        flow = item['_source']['flow']
        contract = item['_source']['contract']
        try:
            knowledge.load_spreadsheet_knowledge_map(
                spreadsheet_api,
                service,
                item,
                notify
            )
        except errors.HttpError, err:
            if err.resp.status in [404, 500]:
                # delete sheet_id from index project and knowledge index
                q = "sheet_id:"+spreadsheetId
                project.delete_by_query(q)
                knowledge.delete_by_query(q)
                logger.warning("==> Spreadsheet %s doesn't exists: %s" % (spreadsheetId, err))
            else:
                # send email to owner
                total_errs += 1
                logger.error("==> exception on %s : %s" % (spreadsheetId, err))
                if notify:
                    subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
                    gmail.send(owner, subject, spreadsheetId, str(err))
        except Exception, e:
            total_errs += 1
            logger.error("==> exception on %s : %s" % (spreadsheetId, e))
            if notify:
                subject = 'ACTION REQUIRED: Tech Gallery %s-%s' % (contract, flow)
                gmail.send(owner, subject, spreadsheetId, str(e))
                # finished output log

    logger.info('%s spreadsheets with %s errors' % (total_hits, total_errs))

if __name__ == '__main__':
    load_knowledge_map(sheet=sheet, notify=notify)
