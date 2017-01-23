from config import Config
import unittest

class ConfigTestCase(unittest.TestCase):
    def test_has_gateway_config(self):
        """Config Test: has gateway config."""
    	c = Config()
        value = c.get('TECHGALLERY_ENDPOINT')
        self.assertEquals(value, 'https://tech-gallery.appspot.com/_ah/api/rest/v1')
