from server import app, security

import requests
from flask import jsonify

@app.route('/api/technologies/<id>')
@security.login_authorized
def get_technology(user, id):
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology/%s' % id
  headers = {'Authorization': user['oauth_token']}
  response = requests.get(url=url, headers= headers)

  return jsonify(response.json())

@app.route('/api/technologies/')
@security.login_authorized
def technologies(user):
  url = 'https://tech-gallery.appspot.com/_ah/api/rest/v1/technology'
  headers = {'Authorization': user['oauth_token']}
  response = requests.get(url=url, headers= headers)

  return jsonify(response.json())