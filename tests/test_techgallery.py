"""TechGaller Unit Test."""
from config import Config
from techgallery import TechGallery
import techgallery
import unittest
import os


class TechGalleryTestCase(unittest.TestCase):
    """TechGallery: Test cases."""

    def setUp(self):
        """Setup API settings for tests."""
        resource_path = os.path.join(
            os.path.split(__file__)[0], "resources/config.yaml")
        self.techgallery = TechGallery(Config(resource_path))

    def test_profile_statuscode_ok(self):
        """TechGallery: load profile for mlacerda return status 200."""
        result, status_code = self.techgallery.profile('mlacerda')
        self.assertEquals(200, status_code)

    def test_profile_statuscode_notok(self):
        """TechGallery: load profile for mlacerda return status not 200."""
        result, status_code = self.techgallery.profile('kdkdkdk')
        self.assertNotEquals(200, status_code)
        print status_code

    def test_load_technology_by_id(self):
        """TechGallery: load technology for id."""
        techs, status_code = self.techgallery.profile('mlacerda')

        self.assertIn('technologies', techs)

        if 'technologies' in techs:
            tech = techs['technologies'][0]
            tech_name = tech['technologyName']
            tech_key = techgallery.convert_name_to_id(tech_name)
            technology, status_code = self.techgallery.technology(tech_key)
            self.assertEquals(200, status_code)
            self.assertEquals(tech_key, technology['id'])
            self.assertIsNotNone(technology['name'])

    def test_name_with_dot(self):
        """TechGallery: Test converter for name with dot character."""
        tech_name = 'VB .Net'
        tech_key = techgallery.convert_name_to_id(tech_name)
        self.assertEquals('vb_net', tech_key)

    def test_name_black_list(self):
        """TechGallery: Test converter for blacklist calabash."""
        tech_name = 'calabash'
        tech_key = techgallery.convert_name_to_id(tech_name)
        self.assertEquals('cabalash', tech_key)

    def test_name_with_space(self):
        """TechGallery: Test converter for name with space character."""
        tech_name = 'Angular JS'
        tech_key = techgallery.convert_name_to_id(tech_name)
        self.assertEquals('angular_js', tech_key)

    def test_name_with_no_ascii(self):
        """TechGallery: Test converter for name with no-ascii character."""
        tech_name = 'Java API for XML (JAX-WS)'
        tech_key = techgallery.convert_name_to_id(tech_name)
        self.assertEquals('java_api_for_xml_(jax-ws)', tech_key)
