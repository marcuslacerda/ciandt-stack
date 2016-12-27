"""Spreadsheet Class."""
import logging
import os

import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

logger = logging.getLogger('stack')

SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
# except ImportError:
#     flags = None


class Spreadsheet(object):
    """"KnowledgeMap Operations.

    Class to manage all operations of people. This class expect a
    config like this:

    If modifying these scopes, delete your previously saved credentials
    at ~/.credentials/sheets.googleapis.com-python-quickstart.json
    """

    def __init__(self, flags):
        """Init using config object."""
        self.flags = flags

    def get_credentials(self):
        """Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.resources')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            resource_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
            flow = client.flow_from_clientsecrets(resource_path, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:
                # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)

        return credentials

    def formatFloat(self, value):
        """Format a string value to a float number."""
        if value.find(',') == -1:
            # convert string br to float
            return float(value)
        else:
            return float(value.replace(',', '.'))

    def read_sheet_data(self, spreadsheetId, values):
        """Read sheet data from value spreadsheet."""
        items = []
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            doc = {
             'technology': row[0],
             'tower': row[1],
             'contract': row[2],
             'flow': row[3],
             'gap': int(row[4]),
             'weight': int(row[5]),
             'necessity': int(row[6]),
             'requirement': int(row[7]),
             'relevancy': self.formatFloat(row[8]),
             'skill_index': self.formatFloat(row[9]),
             'achieve': int(row[10]),
             'sheet_id': spreadsheetId
            }
            items.append(doc)
        return items

    def get_service_spreadsheets(self):
        """Get service spreadsheet API using a authorized request."""
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        service = discovery.build(
            'sheets',
            'v4',
            http=http,
            discoveryServiceUrl=discoveryUrl)

        return service
