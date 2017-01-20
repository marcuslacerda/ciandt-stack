from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import json

SCOPES = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/Users/marcuslacerda/Downloads/knowledgemap_service_account.json', SCOPES)

# Authorize the httplib2.Http object with our credentials
h = credentials.authorize(Http())
# h = Http())

print credentials.access_token

tc_url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'
# headers = {'Authorization': user['oauth_token']}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}
body = ''

# h = Http()
response, content = h.request(
        tc_url,
        method='GET',
        headers=headers)

print response.status
print content


# profile = json.loads(content)
# print profile
