""""TechGallery class."""
import requests
import re


class TechGallery(object):
    """TechGallery operations."""

    def __init__(self, config):
        """Init object.

        Config object must have a TECHGALLERY_ENDPOINT like this
        https://tech-gallery.appspot.com/_ah/api/rest/v1
        """
        self.config = config
        self.endpoint = config.get('TECHGALLERY_ENDPOINT')

    def profile(self, login):
        """Get a profile data by login.

        If profile was not found, then return status_code 404
        """
        url = '%s/profile?email=%s@ciandt.com' % (self.endpoint, login)
        response = requests.get(url=url)
        # TODO: throw exception if response.status_code <> 200
        return response.json(), response.status_code

    def technology(self, id):
        """Get details about technology.

        If profile was not found, then return status_code 404
        """
        url = '%s/technology/%s' % (self.endpoint, id)
        response = requests.get(url=url)

        return response.json(), response.status_code


black_list = {
    'backbone.js': 'backbone.js',
    'calabash': 'cabalash',
    'node.js': 'node.js',
    'asp.net core': 'asp.net_core',
    'asp.net webforms': 'asp.net_webforms',
    'asp.net webapi': 'asp.net_webapi',
    'asp.net mvc': 'asp.net_mvc',
    'quartz.net': 'quartz.net'
}


def convert_name_to_id(tech_name):
    r"""Convert technology name to id.

    This method make a string replace using a bellow rules
    public String convertNameToId(String name) {
        name = Normalizer.normalize(name, Normalizer.Form.NFD);
        name = name.replaceAll("[^\\p{ASCII}]", "");
        return name.toLowerCase()
            .replaceAll(" ", "_")
            .replaceAll("#", "_")
            .replaceAll("\\/", "_")
            .replaceAll("\\.", "");
      }

    """
    if tech_name:
        if tech_name.lower() in black_list:
            tech_key = black_list[tech_name.lower()]
        else:
            tech_key = re.sub('[#/ ]', '_', re.sub(
                '[^\x00-\x7F]', '_', re.sub(
                    '[.]', '', tech_name.lower())))

        return tech_key
