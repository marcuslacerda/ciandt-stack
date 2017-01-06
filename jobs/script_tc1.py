from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import json

scopes = ['https://www.googleapis.com/auth/userinfo.profile']

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    '/Users/marcuslacerda/Downloads/Stack-b8993f313544.json', scopes)



# Authorize the httplib2.Http object with our credentials
h = credentials.authorize(Http())
# h = Http())

tc_url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'
# headers = {'Authorization': user['oauth_token']}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}
body = ''

response, content = h.request(
        tc_url,
        method='GET',
        headers=headers)

print response.status
print content


profile = json.loads(content)
print profile
