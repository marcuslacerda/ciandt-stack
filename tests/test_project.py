"""Project Unit Test."""
from config import Config
from knowledge import Project
import unittest
import os
import mock_util


class ProjectTestCase(unittest.TestCase):
    """Project Tests Cases."""

    def setUp(self):
        """Setup API settings for tests."""
        resource_path = os.path.join(
            os.path.split(__file__)[0], "resources/config.yaml")
        config = Config(resource_path)
        self.project = Project(Config(resource_path))

        id = "12MK2sfe8qwkyLFi7KWudnAsyYF2kteUCWNk4hX2fB4Y"
        self.doc = mock_util.build_project_jeb(id)
        mock_util.post(
            config.get('KNOWLEDGE_ELASTICSEARCH_HOST'),
            'project',
            'settings',
            self.doc['sheet_id'],
            self.doc
        )

    def test_get_technology_list(self):
        """Project: get technolgy list from sheet_id."""
        tech_list = self.project.get_technology_list(self.doc['sheet_id'])
        self.assertGreater(len(tech_list), 0)
