import json
import webbrowser

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.resources/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'
CLIENT_SECRET_FILE = 'tc_client_secret.json'
CREDENTIAL_FILE = 'tc-python-credential.json'

APPLICATION_NAME = 'Gmail API Python Quickstart'

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    flags = parser.parse_args()
except ImportError:
    flags = None

def get_credentials():
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
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILE)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        resource_path = os.path.join(credential_dir, CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(resource_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


if __name__ == '__main__':
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=UTF-8'
    }

    # get credential and authorize http connection
    credentials = get_credentials()
    h = credentials.authorize(httplib2.Http())

    print 'access token %s' % credentials.access_token

    # call google profile API
    # google_profile_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    google_profile_url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    response, content = h.request(
        google_profile_url,
        method='GET',
        headers=headers)

    # json_data = json.loads(content)
    print '==> PROFILE API %s' % response.status
    print content

    tokeninfo_url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
    response, content = h.request(
        '%s?access_token=%s' % (tokeninfo_url, credentials.access_token),
        method='GET',
        headers=headers)

    # json_data = json.loads(content)
    print '==> TOKEN API %s' % response.status
    print content

    # call tech gallery API
    # headers['Authorization'] = 'Bearer %s' % credentials.access_token
    tc_url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'
    response, content = h.request(
        tc_url,
        method='GET',
        headers=headers)

    techs = json.loads(content)
    print '==> TECH GALLERY API %s' % response.status
    if response.status == 200:
        print techs['technologies'][0]
