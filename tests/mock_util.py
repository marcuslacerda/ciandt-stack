"""Mock Util."""
import requests
from datetime import datetime
import json


def build_project_jeb(id):
    """Build mock project object."""
    doc = {
      "@timestamp": "2016-10-17T11:44:13.528Z",
      "sheet_id": id,
      "tower": "umkt_usa_na",
      "contract": "jnj",
      "flow": "jeb",
      "architecture_owner": "arch_login",
      "update_by": "fdewulf",
      "team": [
        "carlosb",
        "cassiop",
        "fpozzer",
        "lcarnieri",
        "freali",
        "fribeiro",
        "fvieira",
        "janine",
        "lisotton",
        "murilol",
        "rodrigoac",
        "wsousa"
      ],
      "stack": [
        "PHP",
        "Drupal",
        "Javascript",
        "Jquery",
        "Gulp",
        "SASS",
        "SMACCS",
        "Bootstrap",
        "SAML",
        "MySql",
        "Docker",
        "Brightcove",
        "Apache Solr",
        "Amazon Web Services AWS",
        "Behat",
        "BEM",
        "GIT"
      ]
    }

    return doc

def post(host, index, doc_type, id, payload):
    """Put payload document for profile API."""
    url = '%s/%s/%s/%s?refresh=wait_for' % (host, index, doc_type, id)
    # json_payload = json.dumps(payload, cls=DateTimeEncoder)
    response = requests.post(url=url, json=payload)

    return response.json(), response.status_code


class DateTimeEncoder(json.JSONEncoder):
    """Handle datetime encoder."""

    def default(self, o):
        """Convert datetime using isoformat datetime method."""
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)
